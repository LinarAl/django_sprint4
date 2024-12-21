from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """Форма для создания поста"""

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('author', )
        widgets = {
            'pub_date': forms.TextInput(attrs={'type': 'datetime-local'})
        }
