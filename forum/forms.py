from bleach import clean
from crispy_forms.helper import FormHelper
from django import forms
from crispy_forms.layout import Submit
from ckeditor.widgets import CKEditorWidget

from .models import Post, Category

ALLOWED_TAGS = ['p', 'i', 'strong', 'em']



class PostForm(forms.ModelForm):
    try:
        categories = forms.ChoiceField(
            widget=forms.RadioSelect,
            choices=[(c.id, c.name) for c in Category.objects.all()],
        )
        image_url = forms.URLField(label='Image URL',
                                   widget=forms.URLInput(attrs={'placeholder': 'Enter Image URL(Optional)'}), required=False)
    except Exception as e:
        print(f"Make migrations error first: {e}")
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
        sanitized_title = clean(title, tags=ALLOWED_TAGS, strip=True)
        return sanitized_title

    def clean_body(self):
        body = self.cleaned_data.get('body')
        sanitized_body = clean(body, tags=ALLOWED_TAGS, strip=True)
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
