from django import forms
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .author import Author
from .genre import Genre
from .series import SeriesCore, SeriesVersion
from .shared import LanguageCodes


class BookCore(models.Model):
    author = models.ManyToManyField(
        Author, verbose_name=_("Author"), related_name="books"
    )
    genres = models.ManyToManyField(
        Genre, verbose_name=_("Genres"), related_name="books"
    )
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
    series = models.ForeignKey(
        SeriesVersion,
        verbose_name=_("Series"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
    )
    cover_image = models.URLField(_("Cover image URL"), max_length=500)
    information_link = models.URLField(_("Information URL"), max_length=500)
    seller_link = models.URLField(_("Seller URL"), max_length=500)
    library_link = models.URLField(_("Library URL"), max_length=500)
    language = models.CharField(
        _("Language"), max_length=2, choices=LanguageCodes.choices
    )
    original_language = models.BooleanField(_("Original language"))
    core = models.ForeignKey(
        BookCore,
        verbose_name=_("Core"),
        on_delete=models.CASCADE,
        related_name="versions",
        blank=True,
    )

    def get_absolute_url(self):
        return reverse_lazy("book", kwargs={"pk": self.pk})

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


class BookVersionForm(forms.ModelForm):
    original_title = forms.CharField(
        required=False, label=_("Original title"), widget=forms.TextInput()
    )

    series_name = forms.CharField(
        required=False, label=_("Series name"), widget=forms.TextInput()
    )

    series_number = forms.IntegerField(
        required=False,
        label=_("Series number"),
        widget=forms.NumberInput(attrs={"min": "1"}),
    )

    author = forms.CharField(required=True, label=_("Author"), widget=forms.TextInput())

    class Meta:
        model = BookVersion
        fields = (
            "title",
            "subtitle",
            "description",
            "series",
            "cover_image",
            "information_link",
            "seller_link",
            "library_link",
            "language",
            "original_language",
            "core",
        )

    def clean(self):
        cleaned = super().clean()

        # Get the authors
        author_names = cleaned.get("author").strip().split(",")
        authors = []
        for author_name in author_names:
            authors.append(Author.objects.get_or_create(name=author_name)[0])

        # Get the core from the original title
        if cleaned.get("original_language"):
            original_title = cleaned.get("title")
        else:
            original_title = cleaned.get("original_title")
        core, created = BookCore.objects.get_or_create(
            versions__title=original_title,
            defaults={"series_number": cleaned.get("series_number")},
        )
        if created:
            core.author.set(authors)
        cleaned["core"] = core

        # Get the series from the series name
        if series_name := cleaned.get("series_name"):
            series, created = SeriesVersion.objects.get_or_create(
                name=series_name,
                language=cleaned.get("language"),
                original_language=cleaned.get("original_language"),
            )
            if created:
                core = SeriesCore.objects.create()
                core.author.set(authors)
                series.core = core
            cleaned["series"] = series

        cleaned.pop("author")
        cleaned.pop("original_title")
        cleaned.pop("series_name")
        cleaned.pop("series_number")

        return cleaned
