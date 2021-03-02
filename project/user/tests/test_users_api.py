from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status # contains some status codes

# constnant url that we are about to test

CREATE_USER_URL = reverse('user:create')

def creatre_user(**params):
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
        creatre_user(**payload)

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