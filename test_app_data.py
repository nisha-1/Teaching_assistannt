# import json
# from teaching_assitant import app


# def test_index_route():
#     response = app.test_client().get('/')

#     assert response.status_code == 200
#     assert response.data.decode('utf-8') == 'Testing, Flask!'
# # def test_signup():
# #     client = app.test_client()

# #     # Test signup with valid credentials
# #     data = {
# #         'name': 'test',
# #         'email': 'test@example.com',
# #         'password': 'password'
# #     }
# #     response = client.post('/signup', data=data)
# #     assert response.status_code == 201

# #     # Test signup with existing email
# #     response = client.post('/signup', data=data)
# #     assert response.status_code == 202

# #     # Test signup with missing fields
# #     data = {
# #         'name': 'test',
# #         'password': 'password'
# #     }
# #     response = client.post('/signup', data=data)
# #     assert response.status_code == 400

# # def test_login():
# #     client = app.test_client()

# #     # Test login with valid credentials
# #     data = {
# #         'email': 'test@example.com',
# #         'password': 'password'
# #     }
# #     response = client.post('/login', data=data)
# #     assert response.status_code == 201

# #     # Test login with invalid credentials
# #     data = {
# #         'email': 'test@example.com',
# #         'password': 'wrongpassword'
# #     }
# #     response = client.post('/login', data=data)
# #     assert response.status_code == 401

# #     # Test login with missing fields
# #     data = {
# #         'email': 'test@example.com',
# #     }
# #     response = client.post('/login', data=data)
# #     assert response.status_code == 400

# # def test_add_ta():
# #     client = app.test_client()

# #     # Test add TA with valid credentials
# #     data = {
# #         'native_english_speaker': True,
# #         'course_instructor': 'John Doe',
# #         'course': 'CS101',
# #         'semester': 'Fall 2023',
# #         'class_size': 50,
# #         'performance_score': 90
# #     }
# #     headers = {'x-access-token': get_token()}
# #     response = client.post('/ta', data=data, headers=headers)
# #     assert response.status_code == 200

# #     # Test add TA with missing fields
# #     data = {
# #         'native_english_speaker': True,
# #         'course_instructor': 24,
# #         'semester': 3,
# #         'class_size': 50,
# #         'performance_score': 90
# #     }
# #     headers = {'x-access-token': get_token()}
# #     response = client.post('/ta', data=data, headers=headers)
# #     assert response.status_code == 400

# # def get_token():
# #     client = app.test_client()
# #     data = {
# #         'email': 'test@example.com',
# #         'password': 'password'
# #     }
# #     response = client.post('/login', data=data)
# #     token = json.loads(response.get_data(as_text=True))['token']
# #     return token
