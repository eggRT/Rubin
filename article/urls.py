from django.urls import path
from .views import create_post_view, EditPostView, detailPost, homeList, deletePost, Search, comments, storyList, LikeView, DislikeView, tags

urlpatterns = [
	path('', homeList, name = "home"),
	path('article/<int:pk>', detailPost, name="detailArticle"),
	path('create/', create_post_view, name = 'createPost'),
	path('search/', Search.as_view(), name='search'),
	path('edit/<int:pk>', EditPostView.as_view(), name = 'editPost'),
	path('editcomment/<int:pk>', comments, name = 'editComment'),
	path('delete/<int:pk>', deletePost, name = 'deletePost'),
	path('storyuser/', storyList, name='storyPost'),
	path('like/<int:pk>', LikeView, name='like_post'),
	path('dislike/<int:pk>', DislikeView, name='dislike_post'),
	path('tag/<slug:tag_slug>', tags, name='tags'),
]
