from django import forms

from .models import MyFeedContent


from django import forms
from datetime import datetime
from .models import MyFeedContent


class FeedForm(forms.ModelForm):
    url = forms.URLField(label='RSS Feed URL',
                         widget=forms.URLInput(attrs={'placeholder': 'Enter RSS Feed URL'}))
    pub_date = forms.DateTimeField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if not url:
            raise forms.ValidationError("This field is required.")
        if MyFeedContent.objects.filter(url=url, user=self.user).exists():
            raise forms.ValidationError("This feed has already been added.")
        return url

    def save(self, commit=True):
        self.instance.pub_date = datetime.now()
        return super().save(commit)

    class Meta:
        model = MyFeedContent
        fields = ['url']




