#!/usr/bin/env python3
"""
Simple test script to verify the authentication fixes
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_authentication():
    print("Testing authentication fixes...")
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # 1. Get CSRF token
    print("\n1. Getting CSRF token...")
    try:
        csrf_response = session.get(f"{BASE_URL}/api/accounts/csrf-token/")
        if csrf_response.status_code == 200:
            csrf_token = csrf_response.json().get('csrfToken')
            print(f"✅ CSRF token obtained: {csrf_token[:20]}...")
            session.headers.update({'X-CSRFToken': csrf_token})
        else:
            print(f"❌ Failed to get CSRF token: {csrf_response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error getting CSRF token: {e}")
        return
    
    # 2. Test current user endpoint without authentication
    print("\n2. Testing current user endpoint without authentication...")
    try:
        current_user_response = session.get(f"{BASE_URL}/api/accounts/current-user/")
        if current_user_response.status_code == 403:
            print("✅ Correctly returns 403 for unauthenticated user")
        else:
            print(f"❌ Unexpected status code: {current_user_response.status_code}")
    except Exception as e:
        print(f"❌ Error testing current user endpoint: {e}")
    
    # 3. Test activities endpoint without authentication
    print("\n3. Testing activities endpoint without authentication...")
    try:
        activities_response = session.get(f"{BASE_URL}/api/accounts/activities/")
        if activities_response.status_code == 403:
            print("✅ Correctly returns 403 for unauthenticated user")
            response_data = activities_response.json()
            if "Authentication credentials were not provided" in response_data.get('detail', ''):
                print("✅ Correct error message returned")
            else:
                print(f"❌ Unexpected error message: {response_data}")
        else:
            print(f"❌ Unexpected status code: {activities_response.status_code}")
    except Exception as e:
        print(f"❌ Error testing activities endpoint: {e}")
    
    print("\n✅ Authentication tests completed!")
    print("\nThe fixes implemented:")
    print("1. ✅ Added CurrentUserView endpoint to check authentication status")
    print("2. ✅ Updated user store with session validation")
    print("3. ✅ Added global axios interceptor for 403 errors")
    print("4. ✅ Updated ProfilePage to use proper authentication checks")
    print("5. ✅ Updated LoginPage to fetch user info after login")
    
    print("\nTo test the full functionality:")
    print("1. Open http://localhost:5173 in your browser")
    print("2. Try to access profile page - should redirect to login")
    print("3. Login with valid credentials")
    print("4. Access profile page - should work without 403 errors")

if __name__ == "__main__":
    test_authentication()
