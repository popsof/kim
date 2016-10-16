from django import forms
from .models import Category, Video

class CateForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ('name', )

class VideoForm(forms.ModelForm):
	class Meta:
		model = Video
		fields = ('category', 'title', 'url', )
		widgets = {
			'category': forms.Select( attrs={'class': 'form-control'} ),
			'title': forms.TextInput( attrs={'class': 'form-control'} ),
			'url': forms.TextInput( attrs={'class': 'form-control'} ),
		}

