from django import forms
from django.utils.translation import gettext_lazy as _

from books.models.book import BookCore

from ..models.book_suggestion import BookSuggestion


class BookSelectWidget(forms.Select):
    template_name = "widgets/book_options.html"
    option_template_name = "widgets/book_option.html"

    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        if value:
            book = self.books.get(value)
            option["book"] = book
        return option


class PitchWidget(forms.Textarea):
    template_name = "widgets/pitch.html"


class BookSuggestionForm(forms.ModelForm):
    class Meta:
        model = BookSuggestion
        fields = ("book", "pitch")
        widgets = {"book": BookSelectWidget(), "pitch": PitchWidget()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        book_field = self.fields["book"]
        book_field.empty_label = None
        book_field.label = _("Select the book you want to suggest")
        book_field.required = True
        book_field.widget.books = {
            b.pk: b for b in BookCore.objects.filter(pk__in=book_field.queryset)
        }
        pitch_field = self.fields["pitch"]
        pitch_field.initial = ""
        pitch_field.label = _("Why should we read this book?")
