from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, Post
from .task import send_assignment_email_task, send_post_notification

# Exercise 3: Signals and Background Tasks¶
# Add signals for post creation
# Implement email notification task
# Test signal triggers

@receiver(post_save, sender=Task)
def task_post_save_handler(sender, instance, created, **kwargs):
    if created:
        assigned_user_emails = instance.assigned_users.values_list('email', flat=True)
        recipient_emails = list(assigned_user_emails)

        if recipient_emails:
            send_assignment_email_task.delay(instance.title, recipient_emails)

@receiver(post_save, sender=Task)
def task_update_handler(sender, instance, created, **kwargs):
    if not created:
        pass

@receiver(post_save, sender=Post)
def post_created_handler(sender, instance, created, **kwargs):
    if created:
        send_post_notification.delay(instance.id)
        

