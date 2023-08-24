from crispy_forms.helper import FormHelper
from django import forms
from crispy_forms.layout import Layout, Div, Field, Submit
# from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from bleach import clean
from django.utils.safestring import mark_safe

from .models import Post, Category

ALLOWED_TAGS = ['p', 'i', 'strong', 'em']


class PostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Post
        fields = ['title', 'body', 'categories']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'title',
            'body',
            Div('categories', css_class='mt-4'),
            Submit('submit', 'Save', css_class='mt-4')  # Adding margin-top
        )

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 10:
            raise forms.ValidationError('Title must be at least 10 characters long.')
        sanitized_title = clean(title, tags=ALLOWED_TAGS, strip=True)
        return sanitized_title

    def clean_body(self):
        body = self.cleaned_data.get('body')
        if '<script>' in body:
            raise forms.ValidationError("Comment cannot contain script tags.")
        sanitized_body = mark_safe(body)
        return sanitized_body


class CommentsForm(forms.Form):
    author = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your Name"
        })
    )
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Leave a comment!"
        }
    ))

    def clean_author(self):
        author = self.cleaned_data['author']
        if any(char.isdigit() for char in author):
            raise forms.ValidationError("Name cannot contain numbers.")
        return author

    def clean_body(self):
        body = self.cleaned_data['body']
        if '<script>' in body:
            raise forms.ValidationError("Comment cannot contain script tags.")
        sanitized_body = clean(body, tags=ALLOWED_TAGS, strip=True)
        return sanitized_body
