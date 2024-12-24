import requests
from random import randint
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserTesting:
    BASE_URL = "http://127.0.0.1:8000"
    
    def __init__(self, users):
        self.users = users
        self.create_user_url = f"{self.BASE_URL}/users"
        self.login_user_url = f"{self.BASE_URL}/login"
        self.send_post_url = f"{self.BASE_URL}/posts"
        self.users_with_token = []
        
    def create_users(self):
        """Create users in the system."""
        for user in self.users:
            try:
                response = requests.post(self.create_user_url, json=user)
                if response.status_code == 201:
                    logger.info(f"User {user['email']} successfully created!")
                else:
                    logger.error(f"Failed to create user {user['email']}. Status code: {response.status_code}")
            except Exception as e:
                logger.error(f"Error creating user {user['email']}: {e}")
    
    def login_users(self):
        """Log in users and store their tokens."""
        for user in self.users:
            login_data = {
                "username": user["email"],
                "password": user["password"]
            }
            try:
                for _ in range(3):  # Retry mechanism
                    login_response = requests.post(self.login_user_url, data=login_data)
                    if login_response.status_code == 200:
                        break
                else:
                    logger.error(f"Failed to login for {user['email']} after retries")
                    continue
                
                # Extract and store token
                token = login_response.json().get("access_token")
                if token:
                    headers = {"Authorization": f"Bearer {token}"}
                    self.users_with_token.append({"email": user["email"], "headers": headers})
                    logger.info(f"Login successful for {user['email']}")
                else:
                    logger.error(f"No token received for {user['email']}")
            
            except Exception as e:
                logger.error(f"Error logging in user {user['email']}: {e}")
    
    def create_posts(self):
        """Create random posts for each logged-in user."""
        if not self.users_with_token:
            logger.warning("No users logged in. Cannot create posts.")
            return
        
        for user in self.users_with_token:
            headers = user["headers"]
            name = user["email"].split('@')[0]
            num_posts = randint(5, 10)
            
            for i in range(num_posts):
                post_data = {
                    "title": f"Post {i + 1} by {name}",
                    "content": f"This is post {i + 1} content from {name}."
                }
                try:
                    post_response = requests.post(self.send_post_url, json=post_data, headers=headers)
                    if post_response.status_code == 201:
                        logger.info(f"Successfully created post {i + 1} for {user['email']}")
                    else:
                        logger.error(f"Failed to create post {i + 1} for {user['email']}. Status code: {post_response.status_code}")
                except Exception as e:
                    logger.error(f"Error creating post {i + 1} for {user['email']}: {e}")
        
    def get_users_with_token(self):
        print(self.users_with_token)
    
    def execute(self):
        """Run the entire flow."""
        self.create_users()
        self.login_users()
        self.create_posts()
        self.get_users_with_token()
        logger.info("Execution complete.")
        
    def login(self):
        self.login_users()
        self.get_users_with_token()
        logger.info("Login complete.")


# Test data
users = [
    {"email": "johndoe@example.com", "password": "Welcome123"},
    {"email": "janesmith@example.com", "password": "Password456"},
    {"email": "michaelbrown@example.com", "password": "EasyPass789"},
    {"email": "emilydavis@example.com", "password": "SecureMe321"},
    {"email": "davidwilson@example.com", "password": "HelloWorld987"},
    {"email": "sophiajohnson@example.com", "password": "ReadAble123"},
    {"email": "chrislee@example.com", "password": "OpenDoor456"},
    {"email": "sarahkim@example.com", "password": "NiceToMeet789"},
    {"email": "jamestaylor@example.com", "password": "AlphaBravo123"},
    {"email": "oliviamartinez@example.com", "password": "SunShine456"}
]


# Instantiate and run the test
user_test = UserTesting(users)
# user_test.execute()
user_test.login()