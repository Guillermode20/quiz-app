from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Question, Score
import random
import logging

# Create your views here.
# views are functions or classes that handle web requests and return web responses

logger = logging.getLogger(__name__)
    
def loadQuestions(request):
    questions = Question.objects.filter(completed=False)
    if questions.exists():
        selected_question = random.choice(questions)
        question = {
            'question_text': selected_question.question_text,
            'option1': selected_question.option1,
            'option2': selected_question.option2,
            'option3': selected_question.option3,
            'option4': selected_question.option4,
            'completed': selected_question.completed,     
        }
        selected_question.completed = True
        selected_question.save()
        
        score, created = Score.objects.get_or_create(id=1)
        
        return render(request, 'quizapp/home.html', question, score.score)
    else:
        return render(request, 'quizapp/end.html')

def checkAnswer(request):
    if request.method == 'POST':
        selected_option = request.POST.get('option')
        logger.info(f"Recieved option: {selected_option}")
        
        if selected_option == 'option1':
            print("Success: Option 1 was selected.")
        elif selected_option == 'option2':
            print("Success: Option 2 was selected.")
        elif selected_option == 'option3':
            print("Success: Option 3 was selected.")
        elif selected_option == 'option4':
            print("Success: Option 4 was selected.")
            
        score, created = Score.objects.get_or_create(id=1)
        score.score += 1
        score.save()
        
        print(f"Success: Score is {score.score}")
        
        return redirect('home')
        
def restart(request):
    if request.method == 'POST':
        if 'restart' in request.POST:
            print("Success: Restart button was clicked.")
            questions = Question.objects.all()
            for question in questions:
                question.completed = False
                question.save()
            return redirect('home')