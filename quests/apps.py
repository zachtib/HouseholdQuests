from django.apps import AppConfig


class QuestsConfig(AppConfig):
    name = 'quests'

    def ready(self):
        import quests.handlers