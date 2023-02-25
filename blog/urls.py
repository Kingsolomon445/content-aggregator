from django.urls import path
from django.views.generic import TemplateView

from .views import *

app_name = 'blog'
urlpatterns = [
    path("", HomePageView.as_view(), name="homepage"),
    path("cyber-security/", CyberSecurityPageView.as_view(), name="cyber-security-page"),
    path("software-development/", SoftwareDevelopmentPageView.as_view(), name="software-development-page"),
    path("ui-ux/", UiUxPageView.as_view(), name="ui-ux-page"),
    path("mobile-pc/", MobilePcPageView.as_view(), name="mobile-pc-page"),
    path("job-updates/", JobUpdatesPageView.as_view(), name="job-updates-page"),
    path("crypto/", CryptoPageView.as_view(), name="crypto-page"),
    path("my-feed/", MyFeedPageView.as_view(), name="my-feed-page"),
    path("add-feed/", AddFeedView.as_view(), name="add-feed-page"),
]
