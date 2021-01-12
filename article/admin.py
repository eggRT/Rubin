from django.contrib import admin
from .models import Post, Profile, Comment, Images, Tag, favoriteTag

class PostImageAdmin(admin.StackedInline):
	model=Images

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	inlines = [PostImageAdmin]

	class Meta:
		model=Post

@admin.register(Images)
class PostImageAdmin(admin.ModelAdmin):
	pass

admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(favoriteTag)
