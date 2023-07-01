from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    score = models.FloatField(default=0)

    class Meta:
        db_table = "company"
