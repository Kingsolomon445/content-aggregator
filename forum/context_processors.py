from forum.models import Post


def get_recent_posts(request):
    recent_posts = Post.objects.order_by('-created_on')[:3]
    return {'recent_posts': recent_posts}