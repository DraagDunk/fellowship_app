from django.db import models
from django.utils.translation import gettext_lazy as _

from .author import Author
from .genre import Genre
from .series import SeriesVersion
from .shared import LanguageCodes

class BookCore(models.Model):

    author = models.ManyToManyField(Author, verbose_name=_("Author"), related_name="books")
    genres = models.ManyToManyField(Genre, verbose_name=_("Genres"), related_name="books")
    series_number = models.PositiveIntegerField()

    @property
    def original_version(self):
        return self.versions.filter(original_language=True).first()

    @property
    def cover_image(self):
        return self.original_version.cover_image

    def __str__(self):
        if original_version := self.versions.filter(original_language=True).first():
            return original_version.title
        else:
            return f"Unknown book ({self.pk})"


class BookVersion(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    subtitle = models.CharField(_("Subtitle"), max_length=100, blank=True)
    description = models.TextField(_("Description"), blank=True)
    series = models.ForeignKey(SeriesVersion, verbose_name=_("Series"), on_delete=models.SET_NULL, null=True, blank=True, related_name="books")
    cover_image = models.URLField(_("Cover image URL"), max_length=500)
    information_link = models.URLField(_("Information URL"), max_length=500)
    seller_link = models.URLField(_("Seller URL"), max_length=500)
    library_link = models.URLField(_("Library URL"), max_length=500)
    language = models.CharField(_("Language"), max_length=2, choices=LanguageCodes.choices)
    original_language = models.BooleanField(_("Original language"))
    core = models.ForeignKey(BookCore, verbose_name=_("Core"), on_delete=models.CASCADE, related_name="versions")

    def __str__(self):
        return self.title

    @property
    def series_number(self):
        return self.core.series_number

    @property
    def author(self):
        return self.core.author

    @property
    def genres(self):
        return self.core.genres

    @property
    def other_versions(self):
        return self.core.versions.exclude(pk=self.pk)