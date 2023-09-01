from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_course_update_email(course_title, user_email):
    subject = 'Обновление материалов курса'
    message = f'Дорогой пользователь, в курсе "{course_title}" появились новые материалы.'
    from_email = 'your@example.com'
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)