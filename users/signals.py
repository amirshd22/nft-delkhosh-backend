from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Userprofile

def create_profile(sender, instance, created, **kwargs):
	if created:
		Userprofile.objects.create(
			user=instance,
            number=instance.username,
			)
            
		print('Profile Created!')
        
post_save.connect(create_profile, sender=User)
