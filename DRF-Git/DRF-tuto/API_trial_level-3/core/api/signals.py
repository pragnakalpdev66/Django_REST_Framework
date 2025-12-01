from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import Post
from django.utils.text import slugify

@receiver(pre_save, sender=Post)
def pre_save_post(sender, instance, **kwargs):
    """Called before Post is saved"""
    if not instance.slug:
        instance.slug = slugify(instance.title)

@receiver(post_save, sender=Post)
def post_save_post(sender, instance, created, **kwargs):
    """Called after Post is saved"""
    if created:
        print(f"New post created: {instance.title}")

@receiver(pre_delete, sender=Post)
def pre_delete_post(sender, instance, **kwargs):
    """Called before Post is deleted"""
    print(f"Post being deleted: {instance.title}")