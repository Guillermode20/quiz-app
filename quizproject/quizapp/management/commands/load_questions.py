import os
import random
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quizproject.settings')
django.setup()

from django.core.management.base import BaseCommand
from quizapp.models import Question
import json

class Command(BaseCommand):
    help = 'Load questions from JSON file'

    def handle(self, *args, **kwargs):
        try:
            with open('questions.json') as f:
                questions_data = json.load(f)
                random.shuffle(questions_data)
                for item in questions_data:
                    Question.objects.create(**item)
            self.stdout.write(self.style.SUCCESS('Successfully loaded questions'))
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'Error decoding JSON: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {e}'))