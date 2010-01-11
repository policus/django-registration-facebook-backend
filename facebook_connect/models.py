from django.db import models
from django.contrib.auth.models import User

class FacebookProfile(models.Model):
    user = models.ForeignKey(User)
    uid = models.CharField(blank=False, max_length=255, null=False)
    