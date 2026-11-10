from django.contrib import admin

from .models import Author, BookCore, BookVersion, Genre, SeriesCore, SeriesVersion


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(BookCore)
class BookCoreAdmin(admin.ModelAdmin):
    list_display = ("original_version", "series_number")

    def original_version(self, obj: BookCore):
        return obj.original_version


@admin.register(BookVersion)
class BookVersionAdmin(admin.ModelAdmin):
    list_display = ("title", "language", "original_language")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(SeriesCore)
class SeriesCoreAdmin(admin.ModelAdmin):
    pass


@admin.register(SeriesVersion)
class SeriesVersionAdmin(admin.ModelAdmin):
    list_display = ("name",)
