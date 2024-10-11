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
    # Initialize the score in the session if it doesn't exist
    if "score" not in request.session:
        request.session["score"] = 0
    if "answered_questions" not in request.session:
        request.session["answered_questions"] = []
    if "questions_answered_count" not in request.session:
        request.session["questions_answered_count"] = 0
    return render(request, "quizapp/startpage.html")


def get_or_create_score(request):
    score = request.COOKIES.get("score", 0)
    return int(score)


def fetch_trivia_questions(amount=10):
    url = "https://opentdb.com/api.php"
    params = {"amount": amount, "type": "multiple", "difficulty": "easy"}

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            trivia_data = response.json()
            trivia_questions = trivia_data["results"]

            if trivia_questions:
                processed_questions = []
                for question in trivia_questions:
                    trivia_question_text = html.unescape(question["question"])
                    trivia_correct_answer = html.unescape(question["correct_answer"])
                    trivia_incorrect_answers = [
                        html.unescape(answer)
                        for answer in question["incorrect_answers"]
                    ]
                    trivia_category = html.unescape(question["category"])

                    all_answers = trivia_incorrect_answers + [trivia_correct_answer]
                    random.shuffle(all_answers)

                    processed_questions.append(
                        {
                            "category_id": trivia_category,
                            "lang": "en",
                            "question": trivia_question_text,
                            "answer": all_answers.index(trivia_correct_answer),
                            "tags": [trivia_category],
                            "answers": all_answers,
                            "source": "OpenTDB",
                        }
                    )

                logger.info(
                    f"Successfully fetched {len(processed_questions)} questions"
                )
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
    cached_questions = cache.get("trivia_questions", [])
    logger.info(f"Current cache size: {len(cached_questions)}")
    if len(cached_questions) < 3:
        logger.info("Fetching new questions for cache")
        new_questions = fetch_trivia_questions()
        cached_questions.extend(new_questions)
        cache.set("trivia_questions", cached_questions)
        logger.info(f"Updated cache size: {len(cached_questions)}")


def get_next_question(request):
    cached_questions = cache.get("trivia_questions", [])
    answered_questions = request.session.get("answered_questions", [])

    for question in cached_questions:
        question_id = f"{question['category_id']}:{question['question']}"
        if question_id not in answered_questions:
            cached_questions.remove(question)
            cache.set("trivia_questions", cached_questions)
            ensure_question_cache()
            return question, question_id

    logger.warning("No new questions available")
    return None, None


def get_trivia_questions(request):
    ensure_question_cache()
    question, question_id = get_next_question(request)

    if question:
        request.session["trivia_answer_mapping"] = question["answers"]
        request.session["trivia_correct_answer"] = question["answers"][
            question["answer"]
        ]
        request.session["current_question_id"] = question_id

        context = {
            "trivia_question_text": question["question"],
            "trivia_correct_answer": question["answers"][question["answer"]],
            "trivia_answers": question["answers"],
            "trivia_category": question["category_id"],
        }

        # Get the stats context and update the main context
        stats_context = get_stats_context(request)
        context.update(stats_context)

        return render(request, "quizapp/trivia.html", context=context)
    else:
        logger.error("Failed to get next question")
        return HttpResponse("No more questions available. Please try again later.")


def check_trivia_answer(request):
    if request.method == "POST":
        selected_option = request.POST.get("option", "")
        answer_mapping = request.session.get("trivia_answer_mapping", [])
        trivia_correct_answer = (
            request.session.get("trivia_correct_answer", "").strip().lower()
        )

        if not answer_mapping:
            logger.error("Answer mapping not found in session")
            return HttpResponse("Error: Answer mapping not found in session")

        # Extract the index from the option string (e.g., 'option2' -> 1)
        try:
            selected_index = int(selected_option.replace("option", "")) - 1
            if 0 <= selected_index < len(answer_mapping):
                selected_answer = answer_mapping[selected_index].strip().lower()
            else:
                logger.error(f"Invalid selected index: {selected_index}")
                return HttpResponse("Error: Invalid answer selection")
        except ValueError:
            logger.error(f"Invalid option format: {selected_option}")
            return HttpResponse("Error: Invalid answer format")

        if selected_answer == trivia_correct_answer:
            score = request.session.get("score", 0)
            score += 1
            request.session["score"] = score

        # Add the current question to the answered questions list
        answered_questions = request.session.get("answered_questions", [])
        current_question_id = request.session.get("current_question_id")
        if current_question_id:
            answered_questions.append(current_question_id)
            request.session["answered_questions"] = answered_questions

        # Increment the questions answered count
        questions_answered_count = request.session.get("questions_answered_count", 0)
        questions_answered_count += 1
        request.session["questions_answered_count"] = questions_answered_count

        request.session.save()  # Explicitly save the session
        return redirect("trivia")
    else:
        return HttpResponse("Invalid request")


def trivia_restart(request):
    if request.method == "POST":
        if "restart" in request.POST:
            request.session["score"] = 0
            request.session["answered_questions"] = []
            request.session["questions_answered_count"] = 0
            request.session.save()  # Explicitly save the session
            cache.delete("trivia_questions")
            ensure_question_cache()

            return redirect("trivia")


def get_stats_context(request):
    current_score = request.session.get("score", 0)
    questions_answered_count = request.session.get("questions_answered_count", 0)
    questions_answered_incorrectly = questions_answered_count - current_score
    accuracy_percentage = (
        (current_score / questions_answered_count) * 100
        if questions_answered_count > 0
        else 0
    )

    accuracy_percentage = round(accuracy_percentage, 1)

    return {
        "current_score": current_score,
        "questions_answered_count": questions_answered_count,
        "questions_answered_incorrectly": questions_answered_incorrectly,
        "accuracy_percentage": accuracy_percentage,
    }


def stats(request):
    context = get_stats_context(request)
    return render(request, "quizapp/stats.html", context)
