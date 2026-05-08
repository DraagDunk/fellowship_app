from django.contrib import admin

from .models.club import Club, ClubMembership

admin.site.register(Club)
admin.site.register(ClubMembership)