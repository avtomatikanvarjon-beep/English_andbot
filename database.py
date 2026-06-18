import json
import os
from typing import List, Dict, Any
from datetime import datetime, timedelta

class Database:
    """Database manager for storing user progress and data"""
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, 'users.json')
        self.progress_file = os.path.join(data_dir, 'progress.json')
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Create data directory and files if they don't exist"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(self.progress_file):
            with open(self.progress_file, 'w') as f:
                json.dump({}, f)
    
    def load_json(self, filename: str) -> Dict[str, Any]:
        """Load JSON data from file"""
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            return {}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    
    def save_json(self, filename: str, data: Dict[str, Any]):
        """Save JSON data to file"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_user(self, user_id: int, username: str, proficiency_level: str) -> bool:
        """Add a new user"""
        users = self.load_json('users.json')
        
        if str(user_id) in users:
            return False
        
        users[str(user_id)] = {
            'username': username,
            'proficiency_level': proficiency_level,
            'created_at': datetime.now().isoformat(),
            'last_seen': datetime.now().isoformat(),
            'lessons_completed': 0,
            'quizzes_completed': 0,
            'vocabulary_learned': 0
        }
        
        self.save_json('users.json', users)
        return True
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Get user information"""
        users = self.load_json('users.json')
        return users.get(str(user_id), {})
    
    def update_user_level(self, user_id: int, proficiency_level: str):
        """Update user's proficiency level"""
        users = self.load_json('users.json')
        if str(user_id) in users:
            users[str(user_id)]['proficiency_level'] = proficiency_level
            self.save_json('users.json', users)
    
    def record_lesson_completion(self, user_id: int, lesson_id: int, level: str):
        """Record that user completed a lesson"""
        progress = self.load_json('progress.json')
        user_key = str(user_id)
        
        if user_key not in progress:
            progress[user_key] = {'lessons': [], 'quizzes': [], 'vocabulary': []}
        
        progress[user_key]['lessons'].append({
            'lesson_id': lesson_id,
            'level': level,
            'completed_at': datetime.now().isoformat()
        })
        
        self.save_json('progress.json', progress)
        
        # Update user stats
        users = self.load_json('users.json')
        if user_key in users:
            users[user_key]['lessons_completed'] = len(progress[user_key]['lessons'])
            self.save_json('users.json', users)
    
    def record_quiz_completion(self, user_id: int, quiz_id: int, score: float, level: str):
        """Record quiz completion with score"""
        progress = self.load_json('progress.json')
        user_key = str(user_id)
        
        if user_key not in progress:
            progress[user_key] = {'lessons': [], 'quizzes': [], 'vocabulary': []}
        
        progress[user_key]['quizzes'].append({
            'quiz_id': quiz_id,
            'score': score,
            'level': level,
            'completed_at': datetime.now().isoformat()
        })
        
        self.save_json('progress.json', progress)
        
        # Update user stats
        users = self.load_json('users.json')
        if user_key in users:
            users[user_key]['quizzes_completed'] = len(progress[user_key]['quizzes'])
            self.save_json('users.json', users)
    
    def record_vocabulary_learned(self, user_id: int, word: str, level: str):
        """Record a learned vocabulary word"""
        progress = self.load_json('progress.json')
        user_key = str(user_id)
        
        if user_key not in progress:
            progress[user_key] = {'lessons': [], 'quizzes': [], 'vocabulary': []}
        
        # Check if word already learned
        if not any(v['word'] == word for v in progress[user_key]['vocabulary']):
            progress[user_key]['vocabulary'].append({
                'word': word,
                'level': level,
                'learned_at': datetime.now().isoformat()
            })
        
        self.save_json('progress.json', progress)
        
        # Update user stats
        users = self.load_json('users.json')
        if user_key in users:
            users[user_key]['vocabulary_learned'] = len(progress[user_key]['vocabulary'])
            self.save_json('users.json', users)
    
    def get_user_progress(self, user_id: int) -> Dict[str, Any]:
        """Get user's learning progress"""
        progress = self.load_json('progress.json')
        return progress.get(str(user_id), {'lessons': [], 'quizzes': [], 'vocabulary': []})
    
    def get_vocabulary(self, level: str) -> List[Dict[str, Any]]:
        """Get vocabulary for a specific level"""
        vocab_data = self.load_json('vocabulary.json')
        return vocab_data.get(level, [])
    
    def get_grammar(self, level: str) -> List[Dict[str, Any]]:
        """Get grammar lessons for a specific level"""
        grammar_data = self.load_json('grammar.json')
        return grammar_data.get(level, [])
    
    def get_daily_lessons(self) -> List[Dict[str, Any]]:
        """Get all daily lessons"""
        lessons_data = self.load_json('daily_lessons.json')
        return lessons_data.get('lessons', [])
    
    def get_quizzes(self, level: str = None) -> List[Dict[str, Any]]:
        """Get quizzes, optionally filtered by level"""
        quizzes_data = self.load_json('quizzes.json')
        quizzes = quizzes_data.get('quizzes', [])
        
        if level:
            quizzes = [q for q in quizzes if q.get('level') == level]
        
        return quizzes
