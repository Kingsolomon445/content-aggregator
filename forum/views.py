from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View, DetailView, ListView
from django.views.generic.edit import FormMixin, DeleteView
from django.urls import reverse, reverse_lazy

from .models import Post, Comments, Category
from .forms import CommentsForm, PostForm


class MyPostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "my_forum_posts.html"
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        # Gets only the posts of the current user and dsiplay
        return Post.objects.filter(author=self.request.user).order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


@method_decorator(csrf_protect, name='dispatch')
class CreatePostView(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        return render(request, 'create_post.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if request.user.is_staff:
                post.is_approved = True
                post.save()
                form.save_m2m()
            else:
                post.save()
            return redirect('forum:index')
        return render(request, 'create_post.html', {'form': form})

@method_decorator(csrf_protect, name='dispatch')
class UpdatePostView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = PostForm(instance=post)
        return render(request, 'update_post.html', {'form': form})

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('forum:post', pk=pk)
        else:
            return render(request, 'update_post.html', {'form': form})


class DeletePostView(DeleteView):
    model = Post
    success_url = reverse_lazy('forum:my-posts')
    template_name = "delete_post.html"

class ForumIndexView(ListView):
    model = Post
    template_name = 'forum_index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(is_approved=True).order_by('-created_on')


class ForumCategoryView(ListView):
    model = Post
    template_name = 'forum_category.html'
    context_object_name = 'posts'
    ordering = ['-created_on']
    paginate_by = 1

    def get_queryset(self):
        category = self.kwargs['category']

        # returns posts that specific to the particular category requested
        return Post.objects.filter(categories__name__exact=category).order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs['category']
        return context

@method_decorator(csrf_protect, name='dispatch')
class ForumPostView(DetailView, FormMixin):
    model = Post
    template_name = 'forum_post.html'
    context_object_name = 'post'
    form_class = CommentsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comments.objects.filter(post=self.object)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = Comments(
            author=form.cleaned_data['author'],
            body=form.cleaned_data['body'],
            post=self.object
        )
        comment.save()
        return redirect(reverse('forum:post', args=(self.object.pk,)))
