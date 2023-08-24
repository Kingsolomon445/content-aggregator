from django.contrib.auth.models import User
from django.db import models

from django.core.validators import URLValidator


# Create your models here.
class BaseModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField(max_length=2000)
    content_name = models.CharField(max_length=100)
    guid = models.CharField(max_length=1000)
    image = models.URLField(null=True, max_length=2000)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.content_name}: {self.title}"


class GeneralContent(BaseModel):
    pass


class PythonContent(BaseModel):
    pass


class SoftwareDevelopmentContent(BaseModel):
    pass


class CyberSecurityContent(BaseModel):
    pass


class UiUxContent(BaseModel):
    pass


class MobilePcContent(BaseModel):
    pass


class JobUpdatesContent(BaseModel):
    pass

class CryptoContent(BaseModel):
    pass
