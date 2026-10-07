from django.db import models
from django.utils.translation import gettext_lazy as _

from .author import Author
from .shared import LanguageCodes

class SeriesCore(models.Model):
    author = models.ManyToManyField(Author)

    def __str__(self):
        if original_version := self.versions.filter(original_language=True).first():
            return original_version.name
        else:
            return f"Unknown series ({self.pk})"


class SeriesVersion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    language = models.CharField(max_length=2, choices=LanguageCodes.choices)
    original_language = models.BooleanField(_("Original language"))
    core = models.ForeignKey(SeriesCore, related_name="versions", on_delete=models.CASCADE)

    def __str__(self):
        return self.name