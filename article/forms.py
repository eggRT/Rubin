from django import forms
from .models import Post, Comment

class postForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('textPost', 'imagePost', 'author')

		widgets = {
			'textPost': forms.Textarea(attrs={'class': 'form-control'}),
			'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'nikc', 'type':'hidden'}),
		}

class commentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('content',)

		widgets = {
			'content': forms.TextInput(attrs={'class': 'form-control'}),
		}