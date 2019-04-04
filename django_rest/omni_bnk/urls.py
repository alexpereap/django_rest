from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'omni_bnk'

urlpatterns = [
    # path('', views.index, name='index'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-out/', views.log_out, name='sign_out'),
    # path('login', views.log_in, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', auth_views.LoginView.as_view(
        template_name='omni_bnk/login/log_in.html', 
        redirect_authenticated_user = True), 
        name='login'
    ),
    path('add-movie/', views.add_movie, name='add_movie'),
    path('movie/<int:pk>', views.movie, name="edit_movie"),
    path('api/movies/', views.MovieView.as_view(), name='get_post_movies'),
    path('api/movies/<int:pk>', views.MovieView.as_view(), name='get_delete_update_movie'),
    
]
