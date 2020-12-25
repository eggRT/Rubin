from django import forms
from .models import Post

class postForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'textPost', 'imagePost', 'author')

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'textPost': forms.Textarea(attrs={'class': 'form-control'}),
			'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'nikc', 'type':'hidden'}),
		}