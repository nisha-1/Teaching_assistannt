# import json
# import pytest
# from teaching_assitant import app,db
# from teaching_assitant import TA
# headers = {'x-access-token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiIxNDZlNjNlOS1iZTUwLTQzYjItYWRhNS1hMzM5ZTc4YmY1YjkiLCJleHAiOjE2ODA1MjU0NzF9.NNcscZ81uh1cjj_TU3aCGE7JIVal3THims6WgVM9iuw'}
# @pytest.fixture(scope='module')
# def test_client():
#     app.config['TESTING'] = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
#     with app.test_client() as testing_client:
#         with app.app_context():
#             db.create_all()
#             yield testing_client
#             db.session.remove()
#             db.drop_all()

# ##Add data 
# def test_add_ta(test_client):
#     new_ta_data = {
#         'native_english_speaker':True,
#         'course_instructor':23,
#         'course':3,
#         'semester':4,
#         'class_size':30,
#         'performance_score':3
#     }
#     response = test_client.post('/ta',data=new_ta_data,headers=headers)
#     assert response.status_code == 200

#     ta_id = json.loads(response.data)['id']
#     response = test_client.get(f'/ta/{ta_id}')
#     assert response.status_code == 200
#     assert json.loads(response.data)['native_english_speaker'] == new_ta_data['native_english_speaker']
#     assert json.loads(response.data)['course_instructor'] == new_ta_data['course_instructor']
#     assert json.loads(response.data)['course'] == new_ta_data['course']
#     assert json.loads(response.data)['semester'] == new_ta_data['semester']
#     assert json.loads(response.data)['class_size'] == new_ta_data['class_size']
#     assert json.loads(response.data)['performance_score'] == new_ta_data['performance_score']

# ##Update data
# def test_update_ta(test_client):
#     new_ta_data = {
#         'native_english_speaker':True,
#         'course_instructor':23,
#         'course':3,
#         'semester':4,
#         'class_size':30,
#         'performance_score':3
#     }
#     response = test_client.post('/ta',data = new_ta_data,headers=headers)
#     assert response.status_code == 200
#     ta_id = json.loads(response.data)['id']
#     updated_ta_data = {
#         'native_english_speaker':False,
#         'course_instructor':25,
#         'course':3,
#         'semester':4,
#         'class_size':35,
#         'performance_score':2
#     }
#     response = test_client.put(f'ta/{ta_id}',data= updated_ta_data,headers=headers)
#     assert response.status_code == 200
#     response = test_client.get(f'/ta/{ta_id}')
#     assert response.status_code ==200
#     updated_ta = json.loads(response.data)
#     assert updated_ta['native_english_speaker'] == updated_ta_data['native_english_speaker']
#     assert updated_ta['course_instructor'] == updated_ta_data['course_instructor']
#     assert updated_ta['course'] == updated_ta_data['course']
#     assert updated_ta['semester'] == updated_ta_data['semester']
#     assert updated_ta['class_size'] == updated_ta_data['class_size']
#     assert updated_ta['performance_score'] == updated_ta_data['performance_score']
