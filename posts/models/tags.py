from django.contrib.auth import get_user_model
from django.db import IntegrityError, models

User = get_user_model()

from companies.models import Company

from .post import Post


class PostCompanyTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = "post_company_tag"
        unique_together = (("post", "company"),)
