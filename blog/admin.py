from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(GeneralContent)
admin.site.register(PythonContent)
admin.site.register(CyberSecurityContent)
admin.site.register(SoftwareDevelopmentContent)
admin.site.register(UiUxContent)
admin.site.register(MobilePcContent)
admin.site.register(JobUpdatesContent)
admin.site.register(CryptoContent)
class GeneralContentAdmin(admin.ModelAdmin):
	list_display = ("content_name", "title", "pub_date")
