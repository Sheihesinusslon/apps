import threading

from django.core.mail import EmailMessage

from .models import (
    Blog,
    Portfolio,
    Testimonial,
    Certificate,
    ContactProfile,
    Skill,
)

EMAIL_SUBJECT = "RESUME APP: Contact form submitted."


class ModelFacade:
    """
    Facade design pattern for creating an object that contains all
    existing models for IndexView
    """
    def __init__(self):
        self.skills = Skill.objects.all()
        self.testimonials = Testimonial.objects.filter(is_active=True)
        self.certificates = Certificate.objects.filter(is_active=True)
        self.blogs = Blog.objects.filter(is_active=True)
        self.portfolio = Portfolio.objects.filter(is_active=True)


class EmailThread(threading.Thread):
    """
    Allows to send an email notification to the admin asynchronously
    """
    def __init__(self, email: EmailMessage):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


def create_email_message(instance: ContactProfile) -> str:
    return f"Name: {instance.name}" \
           f"\nEmail: {instance.email}" \
           f"\nMessage: {instance.message}" \
           f"\n\n" \
           f"From: {instance.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
