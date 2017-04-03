from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse

from quests.forms import SpendForm
from quests.models import QuestEntry, QuestProfile


@login_required
def home(request):
    quests = QuestEntry.objects.filter(user=request.user, completed=False)

    return render(request, 'home.html', {
        'quests': quests,
    })


@login_required
def complete(request, quest_id):
    quest = QuestEntry.objects.get(id=quest_id)
    profile = QuestProfile.objects.get(user=request.user)

    if request.method == 'POST':
        quest.completed = True
        profile.balance += quest.template.reward
        profile.save()
        quest.save()
        messages.success(request, f'{quest.template.name} completed!')
        return HttpResponseRedirect(reverse('home'))

    return render(request, 'complete.html', {
        'quest': quest,
    })


@login_required
def spend(request):
    if request.method == 'POST':
        form = SpendForm(request.POST, user=request.user)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if request.user.profile.spend(amount):
                messages.success(request, f'You succesfully spent ${amount}')
                return HttpResponseRedirect(reverse('home'))
            else:
                form.add_error('Not enough money in your reward balance')
    else:
        form = SpendForm(user=request.user)

    return render(request, 'spend.html', {
        'form': form,
        'user': request.user,
    })
