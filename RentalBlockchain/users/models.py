from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	private_key = models.CharField(max_length=100,default='')


def create_user(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()

post_save.connect(create_user, sender = User)
