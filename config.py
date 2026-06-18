import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))

# Proficiency Levels
PROFICIENCY_LEVELS = {
    'A2': {'name': 'Elementary', 'description': 'Basic English'},
    'B1': {'name': 'Pre-Intermediate', 'description': 'Intermediate level'},
    'B2': {'name': 'Intermediate', 'description': 'Upper-Intermediate'},
    'C1': {'name': 'Advanced', 'description': 'Advanced level'},
    'IELTS_5': {'name': 'IELTS 5', 'description': 'IELTS Level 5'},
    'IELTS_6': {'name': 'IELTS 6', 'description': 'IELTS Level 6'},
    'IELTS_7': {'name': 'IELTS 7', 'description': 'IELTS Level 7'}
}

# Quiz Settings
QUIZ_DURATION_SECONDS = 300
QUIZ_QUESTIONS_PER_LESSON = 5

# Daily Lesson Time (24-hour format)
DAILY_LESSON_HOUR = 9
DAILY_LESSON_MINUTE = 0
