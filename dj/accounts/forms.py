from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        profile = kwargs['instance']
        kwargs['initial'] = {
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
        }
        super().__init__(*args, **kwargs)

    def clean_mvp_id(self):
        mvp_id = self.cleaned_data.get('mvp_id')
        if mvp_id:
            qs = Profile.objects.filter(mvp_id=mvp_id)
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(f'This is already registered.')
        return mvp_id

    def clean_docs_tag(self):
        docs_tag = self.cleaned_data.get('docs_tag')
        if docs_tag:
            qs = Profile.objects.filter(docs_tag=docs_tag)
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(f'This is already registered.')
            docs_tag = docs_tag.upper()
        return docs_tag

    def save(self):
        profile = super().save()
        profile.user.first_name = self.cleaned_data['first_name']
        profile.user.last_name = self.cleaned_data['last_name']
        profile.user.save()
        return profile

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'mvp_id',
            'docs_tag',
            'bio',
        ]
