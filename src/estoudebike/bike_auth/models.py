import uuid
from django.contrib.auth.models import User
from django.db import models


class Token(models.Model):
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, db_index=True)

    user = models.ForeignKey(User, null=True, blank=True)
