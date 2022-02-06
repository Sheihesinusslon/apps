import logging

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.dispatch import receiver
from .models import UserProfile, ContactProfile
from .utils import EMAIL_SUBJECT, create_email_message, EmailThread
from app.settings import EMAIL_HOST_USER

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        logger.info("User profile has been created")


@receiver(post_save, sender=ContactProfile)
def contact_created(sender, instance, created, **kwargs):
    if created:
        # Send an email notification
        msg = create_email_message(instance)
        email = EmailMessage(
            EMAIL_SUBJECT,
            msg,
            EMAIL_HOST_USER,
            [EMAIL_HOST_USER],
        )
        EmailThread(email).start()
        logger.info("Contact form submitted, email has been sent.")
