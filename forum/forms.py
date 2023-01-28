from crispy_forms.helper import FormHelper
from django import forms
from crispy_forms.layout import Submit
from ckeditor.widgets import CKEditorWidget
from html_sanitizer import Sanitizer

from .models import Post, Category



class PostForm(forms.ModelForm):
    categories = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[(c.id, c.name) for c in Category.objects.all()],
    )
    image_url = forms.URLField(label='Image URL',
                               widget=forms.URLInput(attrs={'placeholder': 'Enter Image URL(Optional)'}), required=False)

    class Meta:
        model = Post
        fields = ['title', 'body', 'image_url', 'categories']
        widgets = {
            'body': CKEditorWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 10:
            raise forms.ValidationError('Title must be at least 10 characters long.')
        return title



    def clean_body(self):
        # sanitizes the post body from unwanted html tags
        body = self.cleaned_data.get('body')
        sanitizer = Sanitizer()
        sanitized_body = sanitizer.sanitize(body)
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
        # Prevent scripting attacks
        if '<script>' in body:
            raise forms.ValidationError("Comment cannot contain script tags.")
        return body
