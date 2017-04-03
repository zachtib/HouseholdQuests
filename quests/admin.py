from django.contrib import admin

from quests.models import QuestTemplate, QuestProfile, QuestEntry


class QuestTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'reward')


class QuestEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'template', 'date', 'completed')


class QuestProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')


admin.site.register(QuestTemplate, QuestTemplateAdmin)
admin.site.register(QuestEntry, QuestEntryAdmin)
admin.site.register(QuestProfile, QuestProfileAdmin)