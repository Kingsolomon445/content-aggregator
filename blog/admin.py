from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(GeneralContent)
admin.site.register(CyberSecurityContent)
admin.site.register(SoftwareDevelopmentContent)
admin.site.register(UiUxContent)
admin.site.register(MobilePcContent)
admin.site.register(JobUpdatesContent)
admin.site.register(MyFeedContent)
admin.site.register(CryptoContent)

