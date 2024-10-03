from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Question, Score
import random
import logging

# Initialize logger
logger = logging.getLogger(__name__)

# Function to get a random uncompleted question
def get_selected_question():
    questions = Question.objects.filter(completed=False)
    if questions.exists():
        return random.choice(questions)
    return None

# View to load questions for the quiz
def loadQuestions(request):
    selected_question = get_selected_question()
    if selected_question is None:
        return render(request, 'quizapp/end.html')
    
    # Prepare question data for the template
    question = {
        'question_text': selected_question.question_text,
        'option1': selected_question.option1,
        'option2': selected_question.option2,
        'option3': selected_question.option3,
        'option4': selected_question.option4,
        'completed': selected_question.completed,
    }
    
    # Get or create score entry
    score, created = Score.objects.get_or_create(id=1)
    
    # Store the current question text in the session
    request.session['current_question_text'] = selected_question.question_text
    
    return render(request, 'quizapp/home.html', context={'question': question, 'score': score.score})

# View to check the user's answer
def checkAnswer(request):
    if request.method == 'POST':
        selected_option_key = request.POST.get('option').strip().lower()
        
        # Retrieve the current question using the text stored in the session
        current_question_text = request.session.get('current_question_text')
        if current_question_text is None:
            return redirect('home')
        
        try:
            current_question = Question.objects.get(question_text=current_question_text)
            
            if selected_option_key == current_question.correct_answer:
                score, created = Score.objects.get_or_create(id=1)
                score.score += 1
                score.save()
            
            # Mark the question as completed
            current_question.completed = True
            current_question.save()
            
            # Clear the current question text from the session
            del request.session['current_question_text']
            
            return redirect('home')
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
            return redirect('home')