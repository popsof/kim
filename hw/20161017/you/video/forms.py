from django import forms
from .models import Category, Video

class CateForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ('name', )

class VideoAddForm(forms.ModelForm):
	class Meta:
		model = Video
		fields = ('kind', 'key',
					'title', 'desc',
					'published_date', 'thumbnail' )

		widgets = { 'kind': forms.HiddenInput(),
					'key': forms.HiddenInput(),
					'title': forms.HiddenInput(),
					'desc': forms.HiddenInput(),
					'published_date': forms.HiddenInput(),
					'thumbnail': forms.HiddenInput(),
					}
	
class VideoForm(forms.ModelForm):
	class Meta:
		model = Video
		fields = ('category', 'title', 'desc', 'key', )
		widgets = {
			'category': forms.Select( attrs={'class': 'form-control'} ),
			'title': forms.TextInput( attrs={'class': 'form-control'} ),
			'desc': forms.TextInput( attrs={'class': 'form-control'} ),
			'key': forms.HiddenInput(),
			'thumbnail': forms.HiddenInput(),
		}
