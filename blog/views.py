
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.conf import settings

import os
import random

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pass the last 20 contents to templates
        contents = self.model.objects.filter().order_by("-pub_date")[:20]

        # If content doesnt have image , get random image from selected folder
        image_folder = kwargs.get("image_folder", "SD")
        images = os.listdir(os.path.join(settings.BASE_DIR, f'static/images/{image_folder}'))
        for content in contents:
            if content.image:
                content.image = content.image
            else:
                content.random_image = random.choice(images)
                content.random_image = f'images/{image_folder}/{content.random_image}'
        context["contents"] = contents
        return context


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

    def get_context_data(self, **kwargs):
        kwargs["image_folder"] = "Job"
        return super().get_context_data(**kwargs)


@method_decorator(csrf_protect, name='dispatch')
class PythonPageView(HomePageView):
    template_name = "pythonpage.html"
    model = PythonContent

    def get_context_data(self, **kwargs):
        kwargs["image_folder"] = "Python"
        return super().get_context_data(**kwargs)


@method_decorator(csrf_protect, name='dispatch')
class CyberSecurityPageView(HomePageView):
    template_name = "cybersecuritypage.html"
    model = CyberSecurityContent

    def get_context_data(self, **kwargs):
        kwargs["image_folder"] = "cybersecurity"
        return super().get_context_data(**kwargs)


@method_decorator(csrf_protect, name='dispatch')
class SoftwareDevelopmentPageView(HomePageView):
    template_name = "softwaredevelopmentpage.html"
    model = SoftwareDevelopmentContent

    def get_context_data(self, **kwargs):
        kwargs["image_folder"] = "SD"
        return super().get_context_data(**kwargs)


@method_decorator(csrf_protect, name='dispatch')
class UiUxPageView(HomePageView):
    template_name = "ui_uxpage.html"
    model = UiUxContent

    def get_context_data(self, **kwargs):
        kwargs["image_folder"] = "UI"
        return super().get_context_data(**kwargs)


@method_decorator(csrf_protect, name='dispatch')
class MobilePcPageView(HomePageView):
    template_name = "mobile-pcpage.html"
    model = MobilePcContent

    def get_context_data(self, **kwargs):
        kwargs["image_folder"] = "MobilePc"
        return super().get_context_data(**kwargs)

@method_decorator(csrf_protect, name='dispatch')
class CryptoPageView(HomePageView):
    template_name = "cryptopage.html"
    model = CryptoContent

    def get_context_data(self, **kwargs):
        kwargs["image_folder"] = "Crypto"
        return super().get_context_data(**kwargs)