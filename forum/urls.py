
from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.ForumIndexView.as_view(), name='index'),
    path('<int:pk>/', views.ForumPostView.as_view(), name='post'),
    path('<category>/', views.ForumCategoryView.as_view(), name='category'),
    path('create/post/', views.CreatePostView.as_view(), name='create-post'),
    path('update/<int:pk>/', views.UpdatePostView.as_view(), name='update-post'),
    path('delete/<int:pk>/', views.DeletePostView.as_view(), name='delete-post'),
    path('my-posts/all/', views.MyPostView.as_view(), name='my-posts'),
]