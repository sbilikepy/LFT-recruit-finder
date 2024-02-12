from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


@admin.register(Recruiter)
class RecruiterAdmin(UserAdmin):
    list_display = UserAdmin.list_display
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                    )
                },
            ),
        )
    )


@admin.register(Recruit)
class RecruitAdmin(admin.ModelAdmin):
    list_display = ("name", "note", "activity_time_start",
                    "activity_time_end")
    search_fields = ("name",)
    list_filter = ("name",)


admin.site.register(Character)
admin.site.register(Guild)
admin.site.register(Team)
