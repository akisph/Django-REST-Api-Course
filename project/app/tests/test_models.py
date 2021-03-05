from django.test import TestCase
 
from django.contrib.auth import get_user_model  # returns the active user model

from app import models 
from unittest.mock import patch

def sample_user(email='test@testing.com', password='testpass'):
    """ Create a sample user """
    return get_user_model().objects.create_user(email,password)


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

    def test_tag_str(self):
        """ Test the tag string represantation """
        # Practically that test tha we can create a model named Tag
        # But we doing that by checking its string represantation

        tag = models.Tag.objects.create(
            user = sample_user(),
            name = 'Vegan'
        )    

        self.assertEqual(str(tag),tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title) 

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)