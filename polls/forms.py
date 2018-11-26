from django.forms import ModelForm
from .models import Comments

class CommentFrom(ModelForm):
    class Meta:
         model = Comments
         fields = ['comments_text']