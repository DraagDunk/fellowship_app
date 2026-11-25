from django.db.models.signals import post_save

from clubs.models import Club, ClubMembership
from django.dispatch import receiver

from clubs.models.club import ClubEmailTemplate
from clubs.services.email_service import send_welcome_email


@receiver(post_save, sender=Club)
def create_default_welcome_email_template(sender, instance, created, raw, **kwargs):
    """Make sure every newly created club also creates a welcome email template"""
    if created and not raw:
        ClubEmailTemplate.get_or_create_welcome(instance)

@receiver(post_save, sender=ClubMembership)
def send_welcome_to_new_member(sender, instance, created, raw, **kwargs):
    """Send email to new users when they are created."""
    if created and not raw:
        print(f"Created new member {instance}")
        send_welcome_email(instance)
