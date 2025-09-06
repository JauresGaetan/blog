from django.db import models

from config import settings


# Create your models here.

class Blogs(models.Model):
    title = models.CharField(blank=False, max_length=15)
    content = models.TextField()
    image = models.ImageField(upload_to="public/images/")
    date_created = models.DateField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="blogs", null=True)

    def __str__(self):
        return self.title
