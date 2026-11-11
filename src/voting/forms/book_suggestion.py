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


class BookSuggestionForm(forms.ModelForm):
    class Meta:
        model = BookSuggestion
        fields = ("book",)
        widgets = {"book": BookSelectWidget()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field = self.fields["book"]
        field.empty_label = None
        field.label = _("Select the book you want to suggest")
        field.required = True
        field.widget.books = {
            b.pk: b for b in BookCore.objects.filter(pk__in=field.queryset)
        }
