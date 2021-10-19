from django.db import models
from django.contrib.auth import get_user_model


class Link(models.Model):
    user = models.ForeignKey(
        get_user_model(), 
        blank=False, null=False,
        on_delete=models.CASCADE, # delete links on user delete
    )
    created = models.DateTimeField(
        null=True, blank=True,
        auto_now_add=True,
    )
    url = models.URLField(max_length=256)
    check_interval = models.PositiveIntegerField(blank=True, null=False, default=60*60*5) # default interval is 5 minutes