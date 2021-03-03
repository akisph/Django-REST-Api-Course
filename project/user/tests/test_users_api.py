from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status # contains some status codes

# constnant url that we are about to test

CREATE_USER_URL = reverse('user:create') # The URL for creating the user
TOKEN_URL = reverse('user:token') # The URL for get an authantication toke for a user
ME_URL = reverse('user:me') # The url for the specific user handlng (ex.  Change password )


def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """ Test the users API (public) """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ Test creating with valid payload is successfull """
        payload = {
            'email':'test@testing.com',
            'password':'Test123',
            'name':'TestName'
            }
        res = self.client.post(CREATE_USER_URL,payload) # post a request to the API
        
        # Assert that the user stasus degnify CREATED
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)

        # Asssert the previously created User
        user = get_user_model().objects.get(**res.data) # get the response dictionary and return the created user
        self.assertTrue(user.check_password(payload['password']))    
        self.assertNotIn('password',res.data)


    def test_user_exists(self):
        """ Test creating a user already exists fails """
        payload = {
        'email':'test@testing.com',
        'password':'Test123',
        'name':'TestName'
        }    
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short(self):
        """Test that password must be more than 5 characters"""
        
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'pw',
            'name': 'Test',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
    

    # Create test for token authenntication
    def test_create_token_for_user(self):

        """ Test that a token is created for the user """
        payload = {
            'email':'test@testing.com',
            'password':'testpass',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL,payload) # Post request to create a new toke for the user

        # 1st: Check if there is a token data in the response 
        self.assertIn('token',res.data) 

        #2nd: Check if the status is 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ Test token is not created if invalid credentials are given """
        
        payload = {
            'email':'test@testing.com',
            'password':'testpass',
        }
        create_user(**payload)
        payload['password'] = 'wrongpass'
        res = self.client.post(TOKEN_URL,payload)


        # check if token not created 
        self.assertNotIn('token',res.data)

        #Check if status=400 for bad request
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """ Test that token is not create if user doesen't exist """
        payload = {
            'email':'test@testing.com',
            'password':'testpass',
        }
       
        res = self.client.post(TOKEN_URL,payload)


        # check if token not created 
        self.assertNotIn('token',res.data)

        #Check if status=400 for bad request
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_token_missing_field(self):
        """ Test that email and password are required """
        payload = {
            'email':'test@testing.com'
        }
        create_user(**payload)
        payload['password'] = 'wrongpass'
        res = self.client.post(TOKEN_URL,payload)


        # check if token not created 
        self.assertNotIn('token',res.data)

        #Check if status=400 for bad request
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """ Test that aythentication is required for users """
        # SOS ETST
        # 
        res = self.client.get(ME_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        # Before every test we need to signin/login
        self.user = create_user(
            email='test@londonappdev.com',
            password='testpass',
            name='fname',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me URL"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'new name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)      