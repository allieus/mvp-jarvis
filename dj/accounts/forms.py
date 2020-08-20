from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField
from .models import User, Profile


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'name')
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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'mvp_id',
            'docs_tag',
            'bio',
        ]

    def clean_mvp_id(self):
        mvp_id = self.cleaned_data.get('mvp_id')
        if mvp_id:
            if Profile.objects.filter(mvp_id=mvp_id).exists():
                raise forms.ValidationError(f'This is already registered.')
        return mvp_id

    def clean_docs_tag(self):
        docs_tag = self.cleaned_data.get('docs_tag')
        if docs_tag:
            if Profile.objects.filter(docs_tag=docs_tag).exists():
                raise forms.ValidationError(f'This is already registered.')
            docs_tag = docs_tag.upper()
        return docs_tag
