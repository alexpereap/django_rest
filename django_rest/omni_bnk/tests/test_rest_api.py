from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY
import json
import sys
# sys.stderr.write(repr(response.content) + '\n')

from omni_bnk.models import Movie
from omni_bnk.serializers import MovieSerializer

class RestApiTests(TestCase):
    """ Test for getting movies in the API """
    def setUp(self):
        self.movie1 = Movie.objects.create(
                    name="test",
                    director="test",
                    year="2020",
                    recommended="1"
        )

        self.movie2 = Movie.objects.create(
                    name="test2",
                    director="test2",
                    year="2020",
                    recommended="0"
        )

        self.movie3 = Movie.objects.create(
                    name="test3",
                    director="test1",
                    year="2020",
                    recommended="1"
        )
    
        self.credentials = {
                'username':'user',
                'password':'pass'
            }

        User.objects.create_user(**self.credentials)
        u = self.client.login(username='user', password='pass')

    def test_get_all_movies(self):
        """ get all of the movies """
        url = reverse('omni_bnk:get_post_movies')
        response = self.client.get(url)
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        # sys.stderr.write(repr(serializer.data) + '\n')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"movies": serializer.data})
    
    def test_get_recommended_movies(self):
        """ get only recomended movies """
        url = "%s?recommended" % reverse('omni_bnk:get_post_movies')
        response = self.client.get(url)
        movies = Movie.objects.filter(recommended = 1)
        serializer = MovieSerializer(movies, many=True)
        # sys.stderr.write(repr(serializer.data) + '\n')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"movies": serializer.data})
    
    def test_get_one_movie(self):
        """ test getting one single movie"""
        movie = self.movie1
        url = reverse('omni_bnk:get_delete_update_movie', kwargs={'pk':movie.pk})
        response = self.client.get(url)
        serializer = MovieSerializer(movie, many=False)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
    
    def test_post_movie(self):
        """ test post verb to add a movie"""
        payload = {'movie':
            {
                'name': 'test-post',
                'director': 'test',
                'year': '2020',
                'recommended': '1'
            }
        }

        response = self.client.post(
            reverse('omni_bnk:get_post_movies'),
            data = json.dumps(payload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_put_movie(self):
        """ test put verb to update a movie """
        movie = self.movie1
        payload = {'movie':{
            'director': 'test director'
        }}

        response = self.client.put(
            reverse('omni_bnk:get_delete_update_movie', kwargs={'pk': movie.pk}),
            data = json.dumps(payload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_delete_movie(self):
        """ test delete verb to delete a movie """
        movie = self.movie1

        response = self.client.delete(
            reverse('omni_bnk:get_delete_update_movie', kwargs={'pk': movie.pk}),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, 200)
