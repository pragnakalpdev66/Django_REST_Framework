from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Post

# Exercise 3: Signals and Background Tasks¶
# Add signals for post creation
# Implement email notification task
# Test signal triggers

@shared_task
def send_assignment_email_task(task_title, recipient_emails):
    """
    A Celery task to send an email notification when a new task is assigned.
    """
    subject = f'New Task Assigned: {task_title}'
    message = f'You have been assigned a new task: "{task_title}". Please check the system for details.'
    from_email = settings.DEFAULT_FROM_EMAIL
    
    send_mail(subject, message, from_email, recipient_emails, fail_silently=False)
    
    print(f"Sent email for task '{task_title}' to {recipient_emails}")

@shared_task
def send_post_notification(post_id):
    post = Post.objects.get(id=post_id)
    send_mail(
        subject=f'NewPost: {post.title}',
        message=post.content,
        from_email= 'noreply@example.com',
        recipenit_List=['admin@example.com'],
    )
    print(f"Notification sent for post '{post.title}'")
