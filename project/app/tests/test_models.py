from django.test import TestCase
 
from django.contrib.auth import get_user_model  # returns the active user model


class ModelTests(TestCase):
    def test_create_user_with_email_succesful(self):
        """ Test creatinf an new user with email is succesful """

        email =  "test@testing.com"
        password  = "Test123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password)) # Use thsi way because the password is encrypted


    def test_new_user_email_normalized(self):
        """ Test email for a new user is normalized """

        email = 'test@TESTING.com'    
        password  = "Test123"
        user = get_user_model().objects.create_user(email = email,
                                                    password = password)
        self.assertEqual(user.email,email.lower())

    def test_new_user_valid_email(self):
        """ Test creatig user wiht no email creating error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'test123')

    def test_create_new_superuser(self):
        """  Testing creating a superuser """
        user = get_user_model().objects.create_superuser(
            'test@testing.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
