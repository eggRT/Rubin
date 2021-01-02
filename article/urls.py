from django.urls import path
from .views import HomeView, CreatePostView, EditPostView, detailPost

urlpatterns = [
	path('', HomeView.as_view(), name = "home"),
	path('article/<int:pk>', detailPost, name="detailArticle"),
	path('create/', CreatePostView.as_view(), name = 'createPost'),
	path('edit/<int:pk>', EditPostView.as_view(), name = 'editPost'),
]
