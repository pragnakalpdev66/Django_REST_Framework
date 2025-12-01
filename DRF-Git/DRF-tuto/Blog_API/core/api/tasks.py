from celery import shared_task
from .models import Post
from django.core.mail import send_mail

@shared_task
def send_post_notification(post_id):
    post = Post.objects.get(id=post_id)
    send_mail(
        subject=f'NewPost: {post.title}',
        message=post.content,
        from_email= 'noreply@example.com',
        recipenit_List=['admin@example.com'],
    )