from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model for TrailNet with role-based access and profile fields."""

    ROLE_RIDER = 'rider'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = [
        (ROLE_RIDER, 'Rider'),
        (ROLE_ADMIN, 'Trail Admin'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_RIDER,
    )
    contact_number = models.CharField(max_length=20, blank=True)
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True,
    )
    bike_setup = models.CharField(max_length=120, blank=True)

    def is_trail_admin(self):
        return self.role == self.ROLE_ADMIN or self.is_superuser

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
