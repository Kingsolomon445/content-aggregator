from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from .models import *
from .forms import FeedForm


@method_decorator(csrf_protect, name='dispatch')
class AddFeedView(LoginRequiredMixin, CreateView):
    template_name = 'add_feed.html'
    form_class = FeedForm
    success_url = reverse_lazy('blog:add-feed-page')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)




@method_decorator(csrf_protect, name='dispatch')
class HomePageView(ListView):
    template_name = "index.html"
    model = GeneralContent
    paginate_by = 10
    context_object_name = 'contents'

    def get_queryset(self):
        # Excludes the contents without image
        return self.model.objects.exclude(image=None).order_by("-pub_date")



@method_decorator(csrf_protect, name='dispatch')
class MyFeedPageView(HomePageView):
    template_name = "contentpage.html"
    model = MyFeedContent

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Gets feeds belonging to each user
        user_feeds = MyFeedContent.objects.filter(user=self.request.user).order_by("-pub_date")
        context["contents"] = user_feeds
        context["page"] = 'My Personalized feeds'
        return context




@method_decorator(csrf_protect, name='dispatch')
class JobUpdatesPageView(HomePageView):
    template_name = "contentpage.html"
    model = JobUpdatesContent

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = "Job Updates & Startups"
        return context





@method_decorator(csrf_protect, name='dispatch')
class CyberSecurityPageView(HomePageView):
    template_name = "contentpage.html"
    model = CyberSecurityContent

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = "Cyber Security"
        return context



@method_decorator(csrf_protect, name='dispatch')
class SoftwareDevelopmentPageView(HomePageView):
    template_name = "contentpage.html"
    model = SoftwareDevelopmentContent

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = "Software Development"
        return context


@method_decorator(csrf_protect, name='dispatch')
class UiUxPageView(HomePageView):
    template_name = "contentpage.html"
    model = UiUxContent

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = "Ui Ux"
        return context


@method_decorator(csrf_protect, name='dispatch')
class MobilePcPageView(HomePageView):
    template_name = "contentpage.html"
    model = MobilePcContent

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = "Mobile & pc"
        return context


@method_decorator(csrf_protect, name='dispatch')
class CryptoPageView(HomePageView):
    template_name = "contentpage.html"
    model = CryptoContent

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = "Crypto"
        return context
