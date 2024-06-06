from rest_framework.test import APITestCase
from authentication.models import User


class TestModel(APITestCase):
    def test_creates_user(self):
        user = User.objects.create_user('sphe','missmakau9@gmail.com', 'admin123!')
        self.assertIsInstance(user,User)
        self.assertEqual(user.email,'missmakau9@gmail.com')
        
        
    def test_create_super_user(self):
        user = User.objects.create_superuser('sphe','missmakau9@gmail.com', 'admin123!')
        self.assertIsInstance(user,User)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email,'missmakau9@gmail.com')
        
    def test_raises_error_when_no_username_is_supplied(self):
        self.assertRaises(ValueError,User.objects.create_user,username="",email="makausg@gmail",password="admin2")
        self.assertRaisesMessage(ValueError,"The given username must be set")
        
        
    def test_raises_error_when_no_email_is_supplied(self):
        with self.assertRaisesMessage(ValueError,"The given email must be set"):
            User.objects.create_user(username="lele",email="",password="admin2")
            
            
            
    def test_creates_super_with_is_staff_status(self):
        with self.assertRaisesMessage(ValueError,"Superuser must have is_staff=True."):
            User.objects.create_superuser(username="lele",email="missmakau9@gmail.com",password="admin2", is_staff=False)
            
        
        
    def test_creates_super_with_super_user_status(self):
        with self.assertRaisesMessage(ValueError,"Superuser must have is_superuser=True."):
            User.objects.create_superuser(username="lele",email="missmakau9@gmail.com",password="admin2", is_superuser=False)
     