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
    template_name = "myfeedpage.html"
    model = MyFeedContent

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Gets feeds belonging to each user
        user_feeds = MyFeedContent.objects.filter(user=self.request.user)
        context["feeds"] = user_feeds
        return context




@method_decorator(csrf_protect, name='dispatch')
class JobUpdatesPageView(HomePageView):
    template_name = "jobupdatespage.html"
    model = JobUpdatesContent




@method_decorator(csrf_protect, name='dispatch')
class PythonPageView(HomePageView):
    template_name = "pythonpage.html"
    model = PythonContent




@method_decorator(csrf_protect, name='dispatch')
class CyberSecurityPageView(HomePageView):
    template_name = "cybersecuritypage.html"
    model = CyberSecurityContent



@method_decorator(csrf_protect, name='dispatch')
class SoftwareDevelopmentPageView(HomePageView):
    template_name = "softwaredevelopmentpage.html"
    model = SoftwareDevelopmentContent


@method_decorator(csrf_protect, name='dispatch')
class UiUxPageView(HomePageView):
    template_name = "ui_uxpage.html"
    model = UiUxContent


@method_decorator(csrf_protect, name='dispatch')
class MobilePcPageView(HomePageView):
    template_name = "mobile-pcpage.html"
    model = MobilePcContent


@method_decorator(csrf_protect, name='dispatch')
class CryptoPageView(HomePageView):
    template_name = "cryptopage.html"
    model = CryptoContent
