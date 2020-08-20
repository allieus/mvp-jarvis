from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField
from .models import User


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        field_classes = {'username': EmailField}
        help_texts = {
            'username': 'Please enter your email address as username.',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.username
        if commit:
            user.save()
        return user
