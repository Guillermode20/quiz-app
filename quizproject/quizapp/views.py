from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Score
import random
import logging
import requests
import html
import time
from django.core.cache import cache

# Initialize logger
logger = logging.getLogger(__name__)

def startpage(request):
    return render(request, 'quizapp/startpage.html')

def get_or_create_score():
    score, created = Score.objects.get_or_create(id=1)
    return score

def fetch_trivia_questions(amount=10):
    url = "https://opentdb.com/api.php"
    params = {
        'amount': amount,
        'type': 'multiple',
        'difficulty': 'easy'
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            trivia_data = response.json()
            trivia_questions = trivia_data['results']
            
            if trivia_questions:
                processed_questions = []
                for question in trivia_questions:
                    trivia_question_text = html.unescape(question['question'])
                    trivia_correct_answer = html.unescape(question['correct_answer'])
                    trivia_incorrect_answers = [html.unescape(answer) for answer in question['incorrect_answers']]
                    trivia_category = html.unescape(question['category'])
                    
                    all_answers = trivia_incorrect_answers + [trivia_correct_answer]
                    random.shuffle(all_answers)
                    
                    processed_questions.append({
                        'question_text': trivia_question_text,
                        'correct_answer': trivia_correct_answer,
                        'answers': all_answers,
                        'category': trivia_category,
                    })
                
                logger.info(f"Successfully fetched {len(processed_questions)} questions")
                return processed_questions
            else:
                logger.warning("API returned no questions")
        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
        except (KeyError, ValueError) as e:
            logger.error(f"Error processing API response: {str(e)}")
        
        logger.info(f"Retrying... (attempt {attempt + 1} of {max_retries})")
        time.sleep(3)
    
    logger.error("Failed to fetch questions after all retries")
    return []

def ensure_question_cache():
    cached_questions = cache.get('trivia_questions', [])
    logger.info(f"Current cache size: {len(cached_questions)}")
    if len(cached_questions) < 3:
        logger.info("Fetching new questions for cache")
        new_questions = fetch_trivia_questions()
        cached_questions.extend(new_questions)
        cache.set('trivia_questions', cached_questions)
        logger.info(f"Updated cache size: {len(cached_questions)}")

def get_next_question():
    cached_questions = cache.get('trivia_questions', [])
    if cached_questions:
        question = cached_questions.pop(0)
        cache.set('trivia_questions', cached_questions)
        ensure_question_cache()
        return question
    logger.warning("No questions in cache")
    return None

def get_trivia_questions(request):
    ensure_question_cache()
    question = get_next_question()
    
    if question:
        answer_mapping = {f'option{i+1}': answer for i, answer in enumerate(question['answers'])}
        request.session['trivia_answer_mapping'] = answer_mapping
        request.session['trivia_correct_answer'] = question['correct_answer']
        
        current_score = request.session.get('current_score', 0)
        
        return render(request, 'quizapp/trivia.html', context={
            'trivia_question_text': question['question_text'], 
            'trivia_correct_answer': question['correct_answer'],
            'trivia_answers': question['answers'],
            'trivia_category': question['category'],
            'current_score': current_score
        })
    else:
        logger.error("Failed to get next question")
        return HttpResponse('Failed to fetch trivia questions. Please try again later.')

def check_trivia_answer(request):
    if request.method == 'POST':
        selected_option = request.POST.get('option', '').strip().lower()
        answer_mapping = request.session.get('trivia_answer_mapping', {})
        trivia_correct_answer = request.session.get('trivia_correct_answer', '').strip().lower()
        
        if not answer_mapping:
            logger.error("Answer mapping not found in session")
            return HttpResponse('Error: Answer mapping not found in session')

        selected_answer = answer_mapping.get(selected_option, '').strip().lower()
        
        if selected_answer == trivia_correct_answer:
            score = get_or_create_score()
            score.score += 1
            score.save()
            request.session['current_score'] = score.score
        
        return redirect('trivia')
    else:
        return HttpResponse('Invalid request')

def loadQuestions(request):
    ensure_question_cache()
    question = get_next_question()
    if question is None:
        return render(request, 'quizapp/end.html', context={'score': get_or_create_score().score})
    
    question_data = {
        'question_text': question['question_text'],
        'option1': question['answers'][0],
        'option2': question['answers'][1],
        'option3': question['answers'][2],
        'option4': question['answers'][3],
        'category': question['category']
    }
    
    score = get_or_create_score()
    request.session['current_question'] = question
    
    answered_questions_count = request.session.get('answered_questions_count', 0)
    
    if answered_questions_count > 0:
        correct_percentage = (score.score / answered_questions_count) * 100
    else:
        correct_percentage = 0
        
    correct_percentage = round(correct_percentage, 1)
    
    return render(request, 'quizapp/home.html', context={
        'question': question_data,
        'score': score.score,
        'answered_questions_count': answered_questions_count,
        'correct_percentage': correct_percentage,
        'category': question['category']
    })

def checkAnswer(request):
    if request.method == 'POST':
        selected_option = request.POST.get('option', '').strip().lower()
        current_question = request.session.get('current_question', {})
        
        if current_question:
            if selected_option == current_question.get('correct_answer', '').strip().lower():
                score = get_or_create_score()
                score.score += 1
                score.save()
            
            answered_questions_count = request.session.get('answered_questions_count', 0)
            request.session['answered_questions_count'] = answered_questions_count + 1
            
            del request.session['current_question']
            return redirect('loadQuestions')
        else:
            logger.error("Current question not found in session")
            return render(request, 'quizapp/end.html')

def trivia_restart(request):
    if request.method == 'POST':
        if 'restart' in request.POST:
            request.session['current_score'] = 0
            request.session['answered_questions_count'] = 0
            cache.delete('trivia_questions')
            ensure_question_cache()
            
            score = get_or_create_score()
            score.score = 0
            score.save()
            
            return redirect('trivia')