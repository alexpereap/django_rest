from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY

# Create your tests here.

from omni_bnk.models import Movie

class MovieTests(TestCase):

    def setUp(self):
        # creates an user
        self.credentials = {
            'username':'user',
            'password':'pass'
        }
        User.objects.create_user(**self.credentials)

    def create_movie(self):
            return Movie.objects.create(
                name="test",
                director="test",
                year="2020",
                recommended="1"
            )

    def test_create_movie(self):
        """
        Test for Movie Model
        """
        m = self.create_movie()
        self.assertTrue(isinstance(m, Movie))
        self.assertEqual(str(m), m.name)
    
    def test_index_view(self):
        """
        Test login page
        """
        url = reverse('omni_bnk:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign' )
        self.assertTemplateUsed(response, 'omni_bnk/login/log_in.html')
    
    def test_sign_up_view(self):
        """
        Test sign up page
        """
        url = reverse('omni_bnk:sign_up')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')
        self.assertTemplateUsed(response, 'omni_bnk/login/sign_up.html')
    
    def test_sign_up_post(self):
        """
        Test an user sign up
        """
        response = self.client.post(
            reverse('omni_bnk:sign_up'),
            data = {
                'username':'lex',
                'password1':'aTestPassword.2',
                'password2':'aTestPassword.2'
            },
            follow = True
        )
        self.assertEqual(response.status_code, 200 )
        self.assertContains(response, 'User registered succesfully')
    
    def test_sign_up_post_error(self):
        """
        Test an user signup failure
        """
        response = self.client.post(
            reverse('omni_bnk:sign_up'),
            data = {
                'username':'lex',
                'password1':'aTestPassword.2',
                'password2':'aTestPassword.3'
            },
            follow = True
        )
        # sys.stderr.write(repr(response.content) + '\n')
        self.assertEqual(response.status_code, 200 )
        self.assertContains(response, 'The two password fields didn')
    
    def test_sign_up_authenticated(self):
        """
        Test an authenticaded user navigating to the sign up page
        """
        u = self.client.login(username='user', password='pass')
        self.assertTrue(u)
        url = reverse('omni_bnk:sign_up')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome: user')
        self.assertTemplateUsed(response, 'omni_bnk/dashboard/dashboard_index.html')

    def test_add_movie_view(self):
        """
        Test the add movie form can be accesed
        """
        u = self.client.login(username='user', password='pass')
        self.assertTrue(u)
        url = reverse('omni_bnk:add_movie')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add Movie')
        self.assertTemplateUsed(response, 'omni_bnk/dashboard/add_movie.html')
    
    def test_add_movie_save(self):
        """
        Test a movie can be stored from the add movie form
        """
        u = self.client.login(username='user', password='pass')
        self.assertTrue(u)
        url = reverse('omni_bnk:add_movie')
        response = self.client.post(url, data={
                'name':"test",
                'director':"test",
                'year':"2020",
                'recommended':"1"
        }, follow=True)
        self.assertEqual(response.status_code, 200 )
        self.assertContains(response, 'Movie added')
    
    def test_add_movie_save_fail(self):
        """
        Test a movie store failure from the add movie form
        """
        u = self.client.login(username='user', password='pass')
        self.assertTrue(u)
        url = reverse('omni_bnk:add_movie')
        response = self.client.post(url, data={
                'name':"test",
                'director':"test",
                'yearx':"2020",
                'recommended':"1"
        })
        self.assertEqual(response.status_code, 302 )
    
    def test_movie_not_exists(self):
        """
        Test a movie 404 error trying to visit the edit form
        """
        u = self.client.login(username='user', password='pass')
        self.assertTrue(u)
        url = reverse('omni_bnk:edit_movie', kwargs={'pk':4})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404 )
    
    def test_get_movie(self):
        """
        Test getting a movie in the edit form
        """
        movie = self.create_movie()
        u = self.client.login(username='user', password='pass')
        self.assertTrue(u)
        url = reverse('omni_bnk:edit_movie', kwargs={'pk':movie.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200 )
    
    def test_movie_update(self):
        """
        Test updating a movie in the edit form
        """
        movie = self.create_movie()
        u = self.client.login(username='user', password='pass')
        self.assertTrue(u)
        url = reverse('omni_bnk:edit_movie', kwargs={'pk':movie.id})
        response = self.client.post(url, data={
                'name':"test",
                'director':"test",
                'year':"2020",
                'recommended':"1"
        }, follow=True)
        self.assertEqual(response.status_code, 200 )
        self.assertContains(response, 'Movie updated')

    def test_add_movie_update_fail(self):
        """
        Test a movie store failure from the add movie form
        """
        movie = self.create_movie()
        u = self.client.login(username='user', password='pass')
        self.assertTrue(u)
        url = reverse('omni_bnk:edit_movie', kwargs={'pk':movie.id})
        response = self.client.post(url, data={
                'name':"test",
                'director':"test",
                'yearx':"2020",
                'recommended':"1"
        })
        self.assertEqual(response.status_code, 302 )
    
    def test_logout(self):
        """
        Test the logout
        """
        u = self.client.login(username='user', password='pass')
        self.assertTrue(u)
        url = reverse('omni_bnk:sign_out')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200 )
        self.assertTemplateUsed(response, 'omni_bnk/login/log_in.html')
        self.assertContains(response, 'Logged out succesfully')


        