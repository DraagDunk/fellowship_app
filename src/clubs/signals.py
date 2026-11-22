from django.db.models.signals import post_save

from clubs.models import Club
from django.dispatch import receiver

from clubs.models.club import ClubEmailTemplate


@receiver(post_save, sender=Club)
def create_default_welcome_email_template(sender, instance, created, raw, **kwargs):
    """Make sure every newly created club also creates a welcome email template"""
    if created and not raw:
        ClubEmailTemplate.get_or_create_welcome(instance)
