# Trading Discipline Tracker

"""
Track daily trading discipline and habits to improve consistency and rule adherence.
Similar to Traders Mastermind model with daily/weekly habit tracking and progress metrics.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import statistics


@dataclass
class DailyHabit:
    """Represents a daily trading discipline habit"""
    id: str
    name: str
    description: str
    emoji: str
    goal: int  # How many times per week/days
    category: str  # 'risk', 'preparation', 'psychology', 'execution', 'review'
    importance: int  # 1-5 scale


@dataclass
class WeeklyHabit:
    """Represents a weekly trading discipline task"""
    id: str
    name: str
    description: str
    emoji: str
    goal: int  # How many times per week
    category: str


@dataclass
class DailyTracking:
    """Track daily habit completion"""
    date: str  # YYYY-MM-DD
    habit_id: str
    completed: bool
    notes: str = ""


class DisciplineTracker:
    """Main discipline tracking system"""
    
    def __init__(self, config_file: str = "config/discipline_goals.json"):
        """Initialize tracker with configuration"""
        self.config_file = config_file
        self.daily_habits: Dict[str, DailyHabit] = {}
        self.weekly_habits: Dict[str, WeeklyHabit] = {}
        self.tracking: List[DailyTracking] = []
        self.load_configuration()
    
    def load_configuration(self):
        """Load habits and goals from configuration"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            # Load daily habits
            for habit_data in config.get('daily_habits', []):
                habit = DailyHabit(**habit_data)
                self.daily_habits[habit.id] = habit
            
            # Load weekly habits
            for habit_data in config.get('weekly_habits', []):
                habit = WeeklyHabit(**habit_data)
                self.weekly_habits[habit.id] = habit
        except FileNotFoundError:
            print(f"Configuration file {self.config_file} not found. Using empty config.")
    
    def mark_habit_complete(self, date: str, habit_id: str, notes: str = ""):
        """Mark a daily habit as completed"""
        tracking = DailyTracking(
            date=date,
            habit_id=habit_id,
            completed=True,
            notes=notes
        )
        self.tracking.append(tracking)
    
    def mark_habit_incomplete(self, date: str, habit_id: str, notes: str = ""):
        """Mark a daily habit as not completed"""
        tracking = DailyTracking(
            date=date,
            habit_id=habit_id,
            completed=False,
            notes=notes
        )
        self.tracking.append(tracking)
    
    def get_daily_progress(self, date: str) -> Dict:
        """Get progress for a specific day"""
        day_tracking = [t for t in self.tracking if t.date == date]
        
        if not day_tracking:
            return {
                'date': date,
                'completed': 0,
                'total': len(self.daily_habits),
                'completion_rate': 0.0
            }
        
        completed = sum(1 for t in day_tracking if t.completed)
        total = len(self.daily_habits)
        
        return {
            'date': date,
            'completed': completed,
            'total': total,
            'completion_rate': (completed / total * 100) if total > 0 else 0,
            'details': day_tracking
        }
    
    def get_weekly_progress(self, start_date: str) -> Dict:
        """Get week-long progress (7 days)"""
        start = datetime.strptime(start_date, '%Y-%m-%d')
        week_data = {}
        
        for i in range(7):
            current_date = (start + timedelta(days=i)).strftime('%Y-%m-%d')
            week_data[f'Day {i+1}'] = self.get_daily_progress(current_date)
        
        # Calculate weekly statistics
        completion_rates = [data['completion_rate'] for data in week_data.values()]
        avg_completion = statistics.mean(completion_rates) if completion_rates else 0
        
        return {
            'week_start': start_date,
            'days': week_data,
            'average_completion_rate': avg_completion,
            'week_progress': f"{avg_completion:.1f}%"
        }
    
    def get_habit_progress(self, habit_id: str, days: int = 7) -> Dict:
        """Get progress for a specific habit over N days"""
        today = datetime.now()
        habit = self.daily_habits.get(habit_id)
        
        if not habit:
            return {'error': f'Habit {habit_id} not found'}
        
        # Get tracking for last N days
        completions = []
        for i in range(days):
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            completed = any(
                t.date == date and t.habit_id == habit_id and t.completed
                for t in self.tracking
            )
            completions.append(completed)
        
        completed_count = sum(completions)
        completion_rate = (completed_count / days * 100) if days > 0 else 0
        
        return {
            'habit_id': habit_id,
            'habit_name': habit.name,
            'period_days': days,
            'completions': completions,
            'completed_count': completed_count,
            'completion_rate': completion_rate,
            'goal': habit.goal
        }
    
    def get_overall_progress(self, days: int = 7) -> Dict:
        """Get overall discipline progress percentage"""
        today = datetime.now()
        all_completions = []
        
        for i in range(days):
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            daily_prog = self.get_daily_progress(date)
            all_completions.append(daily_prog['completion_rate'])
        
        overall_rate = statistics.mean(all_completions) if all_completions else 0
        
        return {
            'period_days': days,
            'overall_progress_percentage': overall_rate,
            'status': self._get_status(overall_rate),
            'daily_breakdown': all_completions
        }
    
    def _get_status(self, percentage: float) -> str:
        """Get status based on completion percentage"""
        if percentage >= 90:
            return '🌟 Excellent'
        elif percentage >= 75:
            return '✅ Good'
        elif percentage >= 50:
            return '⚠️ Fair'
        else:
            return '❌ Needs Improvement'
    
    def get_category_progress(self, category: str, days: int = 7) -> Dict:
        """Get progress by category (risk, preparation, psychology, etc.)"""
        category_habits = [h for h in self.daily_habits.values() if h.category == category]
        
        if not category_habits:
            return {'error': f'No habits found for category {category}'}
        
        habit_progress = []
        for habit in category_habits:
            prog = self.get_habit_progress(habit.id, days)
            habit_progress.append(prog)
        
        avg_rate = statistics.mean([h['completion_rate'] for h in habit_progress])
        
        return {
            'category': category,
            'habit_count': len(category_habits),
            'habits': habit_progress,
            'category_average': avg_rate
        }
    
    def add_custom_habit(self, habit_id: str, name: str, description: str, 
                        emoji: str, goal: int, category: str, importance: int = 3):
        """Add a new daily habit"""
        habit = DailyHabit(
            id=habit_id,
            name=name,
            description=description,
            emoji=emoji,
            goal=goal,
            category=category,
            importance=importance
        )
        self.daily_habits[habit_id] = habit
    
    def get_violations(self, days: int = 7) -> Dict:
        """Get missed habits (violations) and reason summary"""
        today = datetime.now()
        violations = []
        
        for i in range(days):
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            day_tracking = [t for t in self.tracking if t.date == date]
            
            for habit_id, habit in self.daily_habits.items():
                # Check if habit was tracked
                tracked = any(t.habit_id == habit_id for t in day_tracking)
                
                if tracked:
                    completed = any(
                        t.habit_id == habit_id and t.completed 
                        for t in day_tracking
                    )
                    
                    if not completed:
                        tracking_record = next(
                            t for t in day_tracking if t.habit_id == habit_id
                        )
                        violations.append({
                            'date': date,
                            'habit': habit.name,
                            'category': habit.category,
                            'notes': tracking_record.notes
                        })
        
        return {
            'period_days': days,
            'violation_count': len(violations),
            'violations': violations,
            'most_common_category': self._get_most_common_violation_category(violations)
        }
    
    def _get_most_common_violation_category(self, violations: List[Dict]) -> Optional[str]:
        """Find most frequently violated category"""
        if not violations:
            return None
        
        categories = [v['category'] for v in violations]
        return max(set(categories), key=categories.count)
    
    def get_streak(self, habit_id: str) -> Dict:
        """Get current streak for a habit (consecutive days completed)"""
        today = datetime.now()
        current_streak = 0
        
        for i in range(365):  # Check up to 1 year
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            completed = any(
                t.date == date and t.habit_id == habit_id and t.completed
                for t in self.tracking
            )
            
            if completed:
                current_streak += 1
            else:
                break
        
        return {
            'habit_id': habit_id,
            'habit_name': self.daily_habits.get(habit_id, {}).name if habit_id in self.daily_habits else 'Unknown',
            'current_streak': current_streak,
            'streak_status': '🔥 Hot!' if current_streak >= 3 else '⏱️ Building...'
        }
    
    def export_results(self, filename: str = None) -> Dict:
        """Export all tracking results"""
        if filename is None:
            filename = f"discipline_report_{datetime.now().strftime('%Y%m%d')}.json"
        
        results = {
            'generated_date': datetime.now().isoformat(),
            'overall': self.get_overall_progress(7),
            'this_week': self.get_weekly_progress(
                (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            ),
            'violations': self.get_violations(7),
            'habits': {
                habit_id: self.get_habit_progress(habit_id, 7)
                for habit_id in self.daily_habits.keys()
            },
            'streaks': {
                habit_id: self.get_streak(habit_id)
                for habit_id in self.daily_habits.keys()
            }
        }
        
        return results


# Example usage and testing
if __name__ == "__main__":
    tracker = DisciplineTracker()
    
    # Example: Track today
    today = datetime.now().strftime('%Y-%m-%d')
    
    # This would normally be called as habits are completed throughout the day
    # tracker.mark_habit_complete(today, 'check_economic_calendar')
    # tracker.mark_habit_complete(today, 'higher_timeframe_analysis')
    
    print("Discipline Tracker initialized and ready to use!")
