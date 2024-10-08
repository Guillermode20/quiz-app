from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Question, Score
import random
import logging
import requests

# Initialize logger
logger = logging.getLogger(__name__)

def startpage(request):
    return render(request, 'quizapp/startpage.html')

# Function to get a random uncompleted question
def get_selected_question():
    questions = Question.objects.filter(completed=False)
    if questions.exists():
        return random.choice(questions)
    return None

def get_or_create_score():
    score, created = Score.objects.get_or_create(id=1)
    return score

def get_trivia_questions(request):
    url = "https://opentdb.com/api.php"
    
    params = {
        'amount': 1,
        'type': 'multiple'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        trivia_data = response.json()
        trivia_questions = trivia_data['results']
        
        return render(request, 'quizapp/trivia.html', context={'trivia_questions': trivia_questions})
    else:
        return HttpResponse('Failed to fetch trivia questions')

# View to load questions for the quiz
def loadQuestions(request):
    selected_question = get_selected_question()
    if selected_question is None:
        total_questions = Question.objects.count()
        return render(request, 'quizapp/end.html', context={'score': get_or_create_score().score, 'total_questions': total_questions})
    
    # Prepare question data for the template
    question = {
        'question_text': selected_question.question_text,
        'option1': selected_question.option1,
        'option2': selected_question.option2,
        'option3': selected_question.option3,
        'option4': selected_question.option4,
        'completed': selected_question.completed,
        'category': selected_question.category
    }
    
    # Get or create score entry
    score, created = Score.objects.get_or_create(id=1)
    
    # Store the current question text in the session
    request.session['current_question_text'] = selected_question.question_text
    score = get_or_create_score()
    completed_questions_count = Question.objects.filter(completed=True).count()
    total_questions = Question.objects.count()
    
    if completed_questions_count > 0:
        correct_percentage = (score.score / completed_questions_count) * 100
    else:
        correct_percentage = 0
        
    correct_percentage = round(correct_percentage, 1)
    
    return render(request, 'quizapp/home.html', context={
        'question': question,
        'score': score.score,
        'total_questions': total_questions,
        'completed_questions_count': completed_questions_count,
        'correct_percentage': correct_percentage,
        'category': selected_question.category
    })

# View to check the user's answer
def checkAnswer(request):
    if request.method == 'POST':
        selected_option_key = request.POST.get('option').strip().lower()
        
        # Retrieve the current question using the text stored in the session
        current_question_text = request.session.get('current_question_text')
        
        try:
            current_question = Question.objects.get(question_text=current_question_text)
            
            if selected_option_key == current_question.correct_answer:
                score = get_or_create_score()
                score.score += 1
                score.save()
            
            # Mark the question as completed
            current_question.completed = True
            current_question.save()
            
            # Clear the current question text from the session
            del request.session['current_question_text']
            
            return redirect('loadQuestions')
        except Question.DoesNotExist:
            return render(request, 'quizapp/end.html')
                                                                
# View to restart the quiz
def restart(request):
    if request.method == 'POST':
        if 'restart' in request.POST:
            Question.objects.all().update(completed=False)
            Score.objects.update_or_create(id=1, defaults={'score': 0})
            if 'current_question_text' in request.session:
                del request.session['current_question_text']
            return redirect('loadQuestions')