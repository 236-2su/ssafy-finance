import requests
import json

# 세션 생성
session = requests.Session()

# 1. CSRF 토큰 가져오기
print("1. CSRF 토큰 가져오기...")
csrf_response = session.get('http://localhost:8000/api/accounts/csrf-token/')
print(f"CSRF Response: {csrf_response.status_code}")
if csrf_response.status_code == 200:
    csrf_data = csrf_response.json()
    print(f"CSRF Token: {csrf_data.get('csrfToken')}")
    csrf_token = csrf_data.get('csrfToken')
else:
    print("CSRF 토큰 가져오기 실패")
    exit()

# 2. 로그인 시도
print("\n2. 로그인 시도...")
login_data = {
    'username': 'testuser',
    'password': 'testpass123'
}

# CSRF 토큰을 헤더에 추가
headers = {
    'X-CSRFToken': csrf_token,
    'Content-Type': 'application/json'
}

login_response = session.post(
    'http://localhost:8000/api/accounts/login/',
    json=login_data,
    headers=headers
)

print(f"Login Response: {login_response.status_code}")
print(f"Login Response Data: {login_response.text}")

# 3. 현재 사용자 정보 확인
print("\n3. 현재 사용자 정보 확인...")
user_response = session.get('http://localhost:8000/api/accounts/current-user/')
print(f"Current User Response: {user_response.status_code}")
print(f"Current User Data: {user_response.text}")

# 4. 쿠키 확인
print("\n4. 세션 쿠키 확인...")
for cookie in session.cookies:
    print(f"Cookie: {cookie.name} = {cookie.value}")

# 5. 새로운 CSRF 토큰 가져오기 (로그인 후 변경될 수 있음)
print("\n5. 새로운 CSRF 토큰 가져오기...")
csrf_response2 = session.get('http://localhost:8000/api/accounts/csrf-token/')
if csrf_response2.status_code == 200:
    csrf_data2 = csrf_response2.json()
    csrf_token = csrf_data2.get('csrfToken')
    print(f"New CSRF Token: {csrf_token}")
    headers['X-CSRFToken'] = csrf_token

# 6. 커뮤니티 글 작성 테스트
print("\n6. 커뮤니티 글 작성 테스트...")
post_data = {
    'category': 'free',
    'title': '테스트 글',
    'content': '테스트 내용입니다.'
}

post_response = session.post(
    'http://localhost:8000/api/community/posts/',
    json=post_data,
    headers=headers
)

print(f"Post Response: {post_response.status_code}")
print(f"Post Response Data: {post_response.text}")
