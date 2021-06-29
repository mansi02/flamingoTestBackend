from django.urls import path
from custom_user import views

urlpatterns = [
    path('register', views.AuthRegister.as_view()),
    path('login', views.AuthLogin.as_view()),
    path('delete_user', views.DeleteUser.as_view()),
    path('activate_user', views.ActivateUser.as_view()),
    path('update_user/<int:pk>/', views.UpdateProfilePicture.as_view()),
]
