from django.contrib import admin
from .models import Category, Post, Comments


# Register your models here.

# The following classes are just for customization for what is shown on the admin pages
class PostAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category)
admin.site.register(Post)
