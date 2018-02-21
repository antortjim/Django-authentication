from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):

    # Base it on built-in User class
    # Don't inherit from it.
    # Doing so could screw up the database
    # thinking it has several instances
    # of the same user
    # (one per inheriting classes)
    user=models.OneToOneField(User, on_delete=models.PROTECT)

    # Additional fields
    # Extend with 2 more fields
    # Portfolio and Picture
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    # Instances of this class return to
    # console the username field when printed
    def __str__(self):
        return self.user.username
