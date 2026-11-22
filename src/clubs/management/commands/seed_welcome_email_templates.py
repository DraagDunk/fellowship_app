from django.core.management import BaseCommand

from clubs.models import Club
from clubs.models.club import ClubEmailTemplate


class Command(BaseCommand):
    help = "Create a WELCOME EmailTemplate with defaults for every club that doesn't have one"

    def handle(self, *args, **options):
        for club in Club.objects.all():
            _, created = ClubEmailTemplate.get_or_create_welcome(club)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created welcome template for {club}"))
