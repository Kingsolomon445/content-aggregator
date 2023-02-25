from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.db import models


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


class MyFeedContent(BaseModel):
    url = models.CharField(null=True, max_length=1999, validators=[URLValidator()])
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    last_modified = models.DateTimeField(auto_now=True)


class GeneralContent(BaseModel):
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