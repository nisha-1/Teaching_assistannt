from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
from datetime import datetime,timedelta
from functools import wraps
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SECRET_KEY'] = 'test12349876'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///teaching_data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)  ## it is used to serialize object to and from JSON
ma = Marshmallow(app)

class UserData(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    public_id = db.Column(db.String(50), unique = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique = True)
    password = db.Column(db.String(80))

class TA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    native_english_speaker = db.Column(db.Boolean, nullable=False)
    course_instructor = db.Column(db.VARCHAR(50), nullable=False)
    course = db.Column(db.VARCHAR(50), nullable=False)
    semester = db.Column(db.VARCHAR(50), nullable=False)
    class_size = db.Column(db.Integer, nullable=False)
    performance_score = db.Column(db.Integer, nullable=False)

    def __init__(self, native_english_speaker, course_instructor, course, semester, class_size, performance_score):
        self.native_english_speaker = native_english_speaker
        self.course_instructor = course_instructor
        self.course = course
        self.semester = semester
        self.class_size = class_size
        self.performance_score = performance_score

class TASchema(ma.Schema):
    class Meta:
        fields = ('id', 'native_english_speaker', 'course_instructor', 'course', 'semester', 'class_size', 'performance_score') 

ta_schema = TASchema()
tas_schema = TASchema(many=True)


#decorator for verifying the jwt
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message':'Token is missing !!'}), 401
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
            current_user = UserData.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({
                'message':'Token is invalid'
            })
        
        return f(current_user,*args,**kwargs)
    return decorated

@app.route('/user',methods=['GET'])
@token_required
def get_all_users(current_user):
    users = UserData.query.all()
    output = []
    for user in users:
        output.append({
            'public_id': user.public_id,
            'name':user.name,
            'email':user.email
        })
    return jsonify({'users':output})
@app.route('/login',methods=['POST'])
def login():
    auth = request.form
    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
    
    user = UserData.query.filter_by(email=auth.get('email')).first()
    if not user:
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
    
    if check_password_hash(user.password,auth.get('password')):
        #generate the JWT token
        token = jwt.encode({
            'public_id':user.public_id,
            'exp':datetime.utcnow() + timedelta(minutes=60)
        },app.config['SECRET_KEY'])

        return make_response(jsonify({'token':token.decode('UTF-8')}),201)
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )

# signup route
@app.route('/signup', methods =['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.form
  
    # gets name, email and password
    name, email = data.get('name'), data.get('email')
    password = data.get('password')
  
    # checking for existing user
    user = UserData.query\
        .filter_by(email = email)\
        .first()
    if not user:
        # database ORM object
        user = UserData(
            public_id = str(uuid.uuid4()),
            name = name,
            email = email,
            password = generate_password_hash(password)
        )
        # insert user
        db.session.add(user)
        db.session.commit()
  
        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)

@app.route('/ta',methods=['POST'])
@token_required
def add_ta(current_user):
    data = request.form
    native_english_speaker = bool(data.get('native_english_speaker'))
    course_instructor = data.get('course_instructor')
    course = data.get('course')
    semester = data.get('semester')
    class_size = data.get('class_size')
    performance_score = data.get('performance_score')
    new_ta = TA(native_english_speaker, course_instructor, course, semester, class_size, performance_score)
    db.session.add(new_ta)
    db.session.commit()
    return ta_schema.jsonify(new_ta)
    # return jsonify({'id': new_ta.id, 'message': 'New TA created!'})

@app.route('/ta/<id>',methods=['GET'])
@token_required
def get_ta(current_user,id):
    ta = TA.query.get(id)
    return ta_schema.jsonify(ta)

@app.route('/ta/<id>', methods=['PUT'])
@token_required
def update_ta(current_user, id):
    ta = TA.query.get(id)
    if not ta:
        return jsonify({'message': 'TA not found'}), 404
    if request.is_json:
        data = request.get_json()
        ta.native_english_speaker = data.get('native_english_speaker', ta.native_english_speaker)
        ta.course_instructor = data.get('course_instructor', ta.course_instructor)
        ta.course = data.get('course', ta.course)
        ta.semester = data.get('semester', ta.semester)
        ta.class_size = data.get('class_size', ta.class_size)
        ta.performance_score = data.get('performance_score', ta.performance_score)
        db.session.commit()
        return ta_schema.jsonify(ta)
        # return jsonify({'id': ta.id, 'message': 'Updated TA !'})
    else:
        return jsonify({'message': 'Request Content-Type must be application/json'}), 400


@app.route('/ta/<id>', methods=['DELETE'])
@token_required
def delete_ta(current_user, id):
    ta = TA.query.get(id)
    if ta:
        db.session.delete(ta)
        db.session.commit()
        return jsonify({'message': 'TA record is deleted.'}), 404
    else:
        return jsonify({'message': 'TA record not found.'}), 404

@app.route('/ta',methods=['GET'])
@token_required
def get_tas(current_user):
    all_tas = TA.query.all()
    return jsonify(tas_schema.dump(all_tas,many=True))


if __name__ == "__main__":
    app.run(debug=True)