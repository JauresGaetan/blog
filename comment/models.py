from django.db import models

from blogs.models import Blogs
from users.models import Users


# Create your models here.
class Comments(models.Model):
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE, related_name="comment", null=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="comment", null=False)
    message = models.TextField(null=False)
    date_crated = models.DateField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.message