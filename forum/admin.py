from django.contrib import admin
from .models import Category, Post, Comments
from .forms import PostForm


class PostAdmin(admin.ModelAdmin):
    form = PostForm


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comments)
