from django.db.models.base import post_save

from clubs.forms.club import EmailTemplate
from clubs.models import Club
from django.dispatch import receiver


@receiver(post_save, sender=Club)
def create_default_welcome_email_template(sender, instance, created, **kwargs):
    if created:
        EmailTemplate.objects.get_or_create(
            club=instance,
            template_type=EmailTemplate.EmailTemplateType.WELCOME,
            defaults={
                "subject": EmailTemplate.DEFAULT_WELCOME_SUBJECT,
                "body": EmailTemplate.DEFAULT_WELCOME_BODY
            }
        )

