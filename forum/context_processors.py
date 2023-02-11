from forum.models import Post


def get_recent_posts(request):
    recent_posts = Post.objects.filter(is_approved=True).order_by('-created_on')[:3]
    return {'recent_posts': recent_posts}