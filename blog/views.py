from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from .models import *


@method_decorator(csrf_protect, name='dispatch')
class HomePageView(ListView):
    template_name = "index.html"
    model = GeneralContent
    paginate_by = 20
    context_object_name = 'contents'

    def get_queryset(self):
        return self.model.objects.exclude(image=None).order_by("-pub_date")


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
