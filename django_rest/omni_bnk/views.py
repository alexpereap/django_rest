from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse


from . models import Movie
from . serializers import MovieSerializer
# Create your views here.
def sign_up(req):
    if(req.user.is_authenticated):
        return redirect('omni_bnk:dashboard')

    if req.method == 'GET':
        form = UserCreationForm()
        return render(req, 'omni_bnk/login/sign_up.html', {'form':form})
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            messages.add_message(req, messages.SUCCESS, 'User registered succesfully, you might want to login now!')
            return redirect('omni_bnk:login')
        else:
            return render(req, 'omni_bnk/login/sign_up.html', {'form':form})

@login_required
def dashboard(req):
    return render(req, 'omni_bnk/dashboard/dashboard_index.html')

@login_required
def add_movie(req):
    if req.method == 'GET':
        return render(req, 'omni_bnk/dashboard/add_movie.html')
    if req.method == 'POST':
        movie = Movie(
            name = req.POST.get('name'),
            director = req.POST.get('director'),
            year = req.POST.get('year'),
            recommended = 0 if req.POST.get('recommended') is None else 1
        )
        try:
            movie.save()
            messages.add_message(req, messages.SUCCESS, 'Movie added')
            return redirect('omni_bnk:dashboard')
        except IntegrityError as e:
            messages.add_message(req, messages.ERROR, 'There was a problem adding the movie: {}'.format(e))
            return redirect('omni_bnk:add_movie')

@login_required
def movie(req, pk):
    movie = get_object_or_404(Movie.objects.all(), pk=pk)
    
    if req.method == 'GET':
        return render(req, 'omni_bnk/dashboard/edit_movie.html', {'movie':movie})
    
    if req.method == 'POST':
        movie.name = req.POST.get('name')
        movie.director = req.POST.get('director')
        movie.year = req.POST.get('year')
        movie.recommended = 0 if req.POST.get('recommended') is None else 1

        try:
            movie.save()
            messages.add_message(req, messages.SUCCESS, 'Movie updated')
            return redirect('omni_bnk:edit_movie', pk)
        except IntegrityError as e:
            messages.add_message(req, messages.ERROR, 'There was a problem updating the movie: {}'.format(e))
            return redirect('omni_bnk:edit_movie', pk)

@login_required
def log_out(req):
    logout(req)
    messages.add_message(req, messages.SUCCESS, 'Logged out succesfully')
    return redirect('omni_bnk:login')


### REST API Methods ###

class MovieView(APIView):
    """ Using django rest framework a set of verbs is defined """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, req, pk = None):
        if pk is None:
            if req.GET.get('recommended') is not None:
                movies = Movie.objects.filter(recommended = 1)
            else :
                movies = Movie.objects.all()
            serializer = MovieSerializer(movies, many=True)
            return Response({"movies": serializer.data})
        else:
            movies = get_object_or_404(Movie.objects.all(), pk=pk)
            serializer = MovieSerializer(movies, many=False)
            return Response(serializer.data)
        
    
    def post(self, req):
        movie = req.data.get('movie')
        serializer = MovieSerializer(data=movie)
        if serializer.is_valid(raise_exception=True):
            movie_sabved = serializer.save()
        return Response({"success": "Movie '{}' created succesfully".format(movie_sabved.name)})
    
    def put(self, req, pk):
        saved_movie = get_object_or_404(Movie.objects.all(), pk=pk)
        data = req.data.get('movie')
        serializer = MovieSerializer(instance=saved_movie, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            movie_saved = serializer.save()
        return Response({"success": "Movie '{}' updated successfully".format(movie_saved.name)})
    
    def delete(self, req, pk):
        movie = get_object_or_404(Movie.objects.all(), pk=pk)
        movie.delete()
        return Response({"message": "Movie with id '{}' has been deleted.".format(pk)})

