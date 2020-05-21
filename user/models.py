# import uuid
#
# from django.db import models
# from django.contrib.auth.models import AbstractUser
#
#
# class CustomUser(AbstractUser):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     def __str__(self):
#         return self.email
