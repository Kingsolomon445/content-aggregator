from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import View, DetailView, ListView
from django.views.generic.edit import FormMixin, DeleteView
from django.urls import reverse, reverse_lazy
from django_staff_required.views import StaffRequiredMixin


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from .models import Post, Comments, Category
from .forms import CommentsForm, PostForm


class MyPostView(StaffRequiredMixin, LoginRequiredMixin, ListView):
    model = Post
    template_name = "my_forum_posts.html"
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


@method_decorator(csrf_protect, name='dispatch')
class CreatePostView(StaffRequiredMixin, LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        return render(request, 'create_post.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('forum:index')
        else:
            return render(request, 'create_post.html', {'form': form})


@method_decorator(csrf_protect, name='dispatch')
class UpdatePostView(StaffRequiredMixin, LoginRequiredMixin, View):
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


class DeletePostView(StaffRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('forum:my-posts')
    template_name = "delete_post.html"


class ForumIndexView(ListView):
    model = Post
    template_name = 'forum_index.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_on']


class ForumCategoryView(ListView):
    model = Post
    template_name = 'forum_category.html'
    context_object_name = 'posts'
    ordering = ['-created_on']
    paginate_by = 10

    def get_queryset(self):
        category = self.kwargs['category']
        return Post.objects.filter(categories__name__exact=category)

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
