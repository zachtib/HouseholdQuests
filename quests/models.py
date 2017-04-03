from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


class QuestTemplate(models.Model):
    name = models.CharField(max_length=200)
    reward = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class QuestEntry(models.Model):
    user = models.ForeignKey(User, related_name='quests', on_delete=models.CASCADE)
    template = models.ForeignKey(QuestTemplate, related_name='entries', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def complete(self):
        self.completed = True

        self.user.profile.balance += self.template.reward
        self.user.profile.save()

        self.save()

    class Meta:
        verbose_name_plural = 'Quest Entries'


class QuestProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f'Profile for {self.user}'

    def spend(self, spend_amount: Decimal) -> bool:
        if spend_amount <= self.balance:
            self.balance = self.balance - spend_amount
            self.save()

            return True
        else:
            return False
