# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
#
# from .models import *
#
#
# @admin.register(Recruiter)
# class RecruiterAdmin(UserAdmin):
#     list_display = UserAdmin.list_display
#     fieldsets = UserAdmin.fieldsets
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (
#             (
#                 "Additional info",
#                 {
#                     "fields": (
#                         "first_name",
#                     )
#                 },
#             ),
#         )
#     )
#
#
# @admin.register(Recruit)
# class RecruitAdmin(admin.ModelAdmin):
#     list_display = (
#         "name",
#         # "activity_days_recruit",
#         "activity_time_start",
#         "activity_time_end",
#         "note",
#     )
#     search_fields = ("name",)
#     list_filter = ("name",
#                    # "activity_days_recruit",
#                    "activity_time_start",
#                    "activity_time_end"
#                    )
#
#
# @admin.register(Character)
# class CharacterAdmin(admin.ModelAdmin):
#     list_display = (
#
#         "nickname",
#         "owner",
#         "class_name",
#         "spec_name",
#         "item_lvl",
#         "wcl"
#
#     )
#     search_fields = ("nickname",)
#     list_filter = ("spec_name", "class_name")
#
#
# @admin.register(Guild)
# class GuildAdmin(admin.ModelAdmin):
#     list_display = (
#         "name", "faction", "recruiter", "highest_progress", "apply_link",
#         "wcl_link", "guild_note",
#     )
#     search_fields = ("name",)
#     list_filter = ("name", "highest_progress")
#
#
# @admin.register(Team)
# class TeamAdmin(admin.ModelAdmin):
#     list_display = (
#         "guild",
#         "name",
#         "loot_system",
#         "team_size",
#         "team_progress",
#         # "activity_days_team",
#         "activity_time_start",
#         "activity_time_end",
#     )
#     search_fields = ("name", "guild")
#     list_filter = ("team_progress", "loot_system",
#                    #  "activity_days_team",
#                    )
