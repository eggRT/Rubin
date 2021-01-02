from django.urls import path
from .views import UserRegisterView, CreateUserProfile, ShowProfilePage, EditProfilePage 

urlpatterns = [
	path('register/', UserRegisterView.as_view(), name='register'),
	path('creationpr/', CreateUserProfile.as_view(), name='creationpr'),
	path('<int:pk>/<int:authorid>/profile', ShowProfilePage.as_view(), name='profile_page'),
	path('editpr/<int:pk>', EditProfilePage.as_view(), name='editpr'),
]