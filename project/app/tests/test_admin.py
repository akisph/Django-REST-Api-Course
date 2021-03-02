from django.test import TestCase,Client
from django.contrib.auth import get_user_model

from django.urls import reverse

class AdminSiteTests(TestCase):

    #!!! function that runs before every test we run 
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'admin@testing.com',
            password= 'Test123'
        )
        self.client.force_login(self.admin_user) # client login with user credentials

        self.user = get_user_model().objects.create_user(
            email = 'test@testing.com',
            password = 'Test123',
            name  = 'TestUser Full Name'
        )
    
    def test_users_listed(self):
        """ Test that users are listed on the page """
        url = reverse('admin:app_user_changelist')
        res = self.client.get(url) # http request to url

        self.assertContains(res,self.user.name)
        self.assertContains(res,self.user.email)
        
    def test_user_change_page(self):
        """ Test that user edit page works """
        url = reverse("admin:app_user_change",args = [self.user.id])
        # /admin/app/user/
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    
    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:app_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)