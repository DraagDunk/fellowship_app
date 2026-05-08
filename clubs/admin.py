from django.contrib import admin

from .models.club import Club, ClubMembership

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(ClubMembership)
class ClubMembershipAdmin(admin.ModelAdmin):
    list_display = ("person", "club", "manager")