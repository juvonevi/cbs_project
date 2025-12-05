from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db import connection
from .models import Quest
from .models import Choice
from .models import UserProgress
import random

# Create your views here.
def index():
    return HttpResponse("There is no quests here")

def nextQuest(request, quest_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/sign/')

    if request.method == "POST":
        print(request.POST.get('path'))
        chosen = request.POST.get('path')
        if chosen.isnumeric():
            c = get_object_or_404(Choice, id = chosen)
            altC = request.POST.get('choice1')
            if altC == c:
                altC = request.POST.get('choice2')
            c2 = get_object_or_404(Choice, id = altC)

            success = c.votes / (c2.votes + 0.01) > random.random()
            c.votes += 1

            successText = "Alas thine \"" + c.text + "\" is in vain. Thus..."
            if success:
                successText = "Thee succeed in thine \"" + c.text + "\" and..."
            return questLoader(request, 1, successText) # str(int(quest_id) + 1)
        elif chosen == "CUSTOM":
            customAnswer = request.POST.get('CustomChoice')
            print(customAnswer)
            if customAnswer == "":
                return HttpResponseRedirect("/")
            
            # Code with possibility of SQL INJECTION
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO quests_choice (quest_id, text, votes) " \
                "VALUES (" + str(quest_id) + ", '" + customAnswer +  "', 1);")

            """ Code that fixes possibility of SQL INJECTION(?)
            quest = get_object_or_404(Quest, id=quest_id)
            customChoice = Choice(quest=quest, text=customAnswer, votes=1)
            customChoice.save()
            """

            success = random.random() > 0.55
            successText = "And you " + customAnswer
            if success:
                successText += " succesfully..."
            else:
                successText += " but it doesnt go as expected..." 
            
            uProgress = get_object_or_404(UserProgress, user=request.user)
            uProgress.page += 1
            return questLoader(request, uProgress.page, successText)


    return HttpResponseRedirect("/quest/1")


def quest(request, quest_id):
    uProgress = get_object_or_404(UserProgress, user=request.user)
    quest_id = uProgress.page
    return questLoader(request, quest_id, "")


def questLoader(request, quest_id, success):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/sign/')
    
    uProgress = get_object_or_404(UserProgress, user=request.user)
    if quest_id != uProgress.page:
        return render(request, 'error.html', {'message':'Thee \'re not supposed to be here'})

    quest = get_object_or_404(Quest, id=quest_id)
    choices = get_list_or_404(Choice, quest=quest_id)
    if len(choices) < 2: 
        print("ERROR TOO FEW CHOICES WITH QUEST", quest_id)
    random.shuffle(choices)
    return render(request, 'quests/quest.html', {'quest':quest, 'c0':choices.pop(), 'c1':choices.pop(), 'success':success})
