from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """Profile model for User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    follows = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True)
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """Create or update a Profile when a User is created or updated"""
    profile, created = Profile.objects.get_or_create(user=instance)
    if created:
        # Automatically follow itself
        profile.follows.add(profile)
        print(f"Profile created and self-followed successfully for user: {instance.username}")
    else:
        print(f"Profile retrieved for user: {instance.username}")
class Tweet(models.Model):
    """Tweet model for User"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_tweets', blank=True)
    retweets = models.ManyToManyField(User, related_name='retweeted_tweets', blank=True)
    def __str__(self):
        return self.content[:50] + '...'
