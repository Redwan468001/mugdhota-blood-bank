from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('donner/<str:pk>/', views.donner, name="donner"),
    path('like-post', views.like_post, name='like-post'),
    path('blood-info-add/', views.blood_create_view, name='blood-info-add'),
    path('blood-info-update/<str:pk>/', views.updateBloodInfo, name='blood-info-update'),
    path('bld-info-update/<str:pk>/', views.userBloodInfo, name='bld-info-update'),
    
    path('login/', views.loginPage, name="login"),
    path('register/', views.RegisterUser, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    
    path('profile/<str:username>/', views.Profile, name="profile"),
    path('update-profile/<str:username>/', views.updateUser, name="update-profile"),
    
    path('management-page/', views.management, name="management-page"),
    path('contact-us/', views.Contact, name="contact-us"),
    path('blood-info-add-problem/', views.BloodInfoAddProblem, name="blood-info-add-problem"),
    
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'), # AJAX
]








