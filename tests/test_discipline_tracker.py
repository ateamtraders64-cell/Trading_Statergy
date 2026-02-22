# Tests for Discipline Tracker

import pytest
from datetime import datetime, timedelta
from analysis.discipline_tracker import DisciplineTracker, DailyHabit, WeeklyHabit, DailyTracking


class TestDisciplineTracker:
    """Test discipline tracking functionality"""
    
    def setup_method(self):
        """Set up test tracker"""
        self.tracker = DisciplineTracker()
        # Add sample habits for testing
        self.tracker.add_custom_habit(
            'test_habit_1',
            'Test Habit 1',
            'First test habit',
            '✅',
            goal=10,
            category='risk'
        )
        self.tracker.add_custom_habit(
            'test_habit_2',
            'Test Habit 2',
            'Second test habit',
            '📊',
            goal=10,
            category='preparation'
        )
    
    def test_add_custom_habit(self):
        """Test adding custom habits"""
        initial_count = len(self.tracker.daily_habits)
        
        self.tracker.add_custom_habit(
            'new_habit',
            'New Habit',
            'A new test habit',
            '🎯',
            goal=15,
            category='psychology'
        )
        
        assert len(self.tracker.daily_habits) == initial_count + 1
        assert 'new_habit' in self.tracker.daily_habits
    
    def test_mark_habit_complete(self):
        """Test marking habit as complete"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        self.tracker.mark_habit_complete(today, 'test_habit_1')
        
        day_tracking = [t for t in self.tracker.tracking if t.date == today]
        assert len(day_tracking) > 0
        assert any(t.habit_id == 'test_habit_1' and t.completed for t in day_tracking)
    
    def test_mark_habit_incomplete(self):
        """Test marking habit as incomplete"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        self.tracker.mark_habit_incomplete(today, 'test_habit_2', notes="No time")
        
        day_tracking = [t for t in self.tracker.tracking if t.date == today and t.habit_id == 'test_habit_2']
        assert len(day_tracking) == 1
        assert not day_tracking[0].completed
        assert day_tracking[0].notes == "No time"
    
    def test_daily_progress(self):
        """Test daily progress calculation"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Mark some habits complete
        self.tracker.mark_habit_complete(today, 'test_habit_1')
        self.tracker.mark_habit_incomplete(today, 'test_habit_2')
        
        progress = self.tracker.get_daily_progress(today)
        
        assert progress['date'] == today
        assert progress['completed'] == 1
        assert progress['total'] >= 2
        assert progress['completion_rate'] > 0
    
    def test_habit_progress(self):
        """Test single habit progress over days"""
        today = datetime.now()
        habit_id = 'test_habit_1'
        
        # Complete habit for last 3 days
        for i in range(3):
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            self.tracker.mark_habit_complete(date, habit_id)
        
        progress = self.tracker.get_habit_progress(habit_id, 7)
        
        assert progress['habit_id'] == habit_id
        assert progress['completed_count'] == 3
        assert progress['completion_rate'] >= 40  # 3 out of 7 days
    
    def test_weekly_progress(self):
        """Test weekly progress calculation"""
        today = datetime.now()
        start_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
        
        weekly = self.tracker.get_weekly_progress(start_date)
        
        assert 'week_start' in weekly
        assert 'days' in weekly
        assert len(weekly['days']) == 7
        assert 'average_completion_rate' in weekly
    
    def test_overall_progress(self):
        """Test overall discipline progress"""
        today = datetime.now()
        
        # Add some completions
        for i in range(3):
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            self.tracker.mark_habit_complete(date, 'test_habit_1')
            self.tracker.mark_habit_complete(date, 'test_habit_2')
        
        overall = self.tracker.get_overall_progress(7)
        
        assert 'overall_progress_percentage' in overall
        assert 0 <= overall['overall_progress_percentage'] <= 100
        assert 'status' in overall
    
    def test_category_progress(self):
        """Test category-based progress"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        self.tracker.mark_habit_complete(today, 'test_habit_1')  # risk category
        
        cat_progress = self.tracker.get_category_progress('risk', 1)
        
        assert cat_progress['category'] == 'risk'
        assert 'habits' in cat_progress
        assert 'category_average' in cat_progress
    
    def test_violations_report(self):
        """Test violations tracking"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Mark habit incomplete
        self.tracker.mark_habit_incomplete(today, 'test_habit_1', "Forgot")
        
        violations = self.tracker.get_violations(1)
        
        assert 'violation_count' in violations
        assert 'violations' in violations
        assert len(violations['violations']) >= 1
    
    def test_streak_calculation(self):
        """Test streak calculation"""
        today = datetime.now()
        habit_id = 'test_habit_1'
        
        # Create 5-day streak
        for i in range(5):
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            self.tracker.mark_habit_complete(date, habit_id)
        
        streak = self.tracker.get_streak(habit_id)
        
        assert streak['current_streak'] == 5
        assert 'Hot!' in streak['streak_status']
    
    def test_export_results(self):
        """Test exporting results"""
        results = self.tracker.export_results()
        
        assert 'generated_date' in results
        assert 'overall' in results
        assert 'violations' in results
        assert 'habits' in results
    
    def test_status_emoji_assignment(self):
        """Test status emoji based on percentage"""
        # High performance
        status_high = self.tracker._get_status(95)
        assert '🌟' in status_high or 'Excellent' in status_high
        
        # Medium performance
        status_med = self.tracker._get_status(60)
        assert 'Fair' in status_med
        
        # Low performance
        status_low = self.tracker._get_status(30)
        assert 'Needs Improvement' in status_low


class TestDisciplineReporter:
    """Test reporting functionality"""
    
    def setup_method(self):
        """Set up test tracker and reporter"""
        from analysis.discipline_reporter import DisciplineReporter
        
        self.tracker = DisciplineTracker()
        self.tracker.add_custom_habit('habit_1', 'Habit 1', 'Test', '✅', 10, 'risk')
        self.tracker.add_custom_habit('habit_2', 'Habit 2', 'Test', '📊', 10, 'preparation')
        
        self.reporter = DisciplineReporter(self.tracker)
    
    def test_daily_report_generation(self):
        """Test daily report generation"""
        report = self.reporter.generate_daily_report()
        
        assert 'DAILY DISCIPLINE REPORT' in report
        assert 'Completion Rate' in report
        assert '%' in report
    
    def test_weekly_report_generation(self):
        """Test weekly report generation"""
        report = self.reporter.generate_weekly_report()
        
        assert 'WEEKLY DISCIPLINE REPORT' in report
        assert 'Average Completion Rate' in report
    
    def test_habit_dashboard_generation(self):
        """Test habit dashboard generation"""
        # Mark some habits
        today = datetime.now().strftime('%Y-%m-%d')
        self.tracker.mark_habit_complete(today, 'habit_1')
        
        dashboard = self.reporter.generate_habit_dashboard()
        
        assert 'DAILY HABITS DISCIPLINE TRACKER' in dashboard
        assert 'Habit 1' in dashboard or 'habit_1' in dashboard
        assert 'OVERALL HABIT PROGRESS' in dashboard
    
    def test_violations_report_generation(self):
        """Test violations report"""
        today = datetime.now().strftime('%Y-%m-%d')
        self.tracker.mark_habit_incomplete(today, 'habit_1', 'Busy')
        
        report = self.reporter.generate_violations_report()
        
        assert 'VIOLATIONS' in report
        assert 'violation_count' in report.lower() or 'violations' in report
    
    def test_streak_report_generation(self):
        """Test streak report"""
        today = datetime.now()
        for i in range(3):
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            self.tracker.mark_habit_complete(date, 'habit_1')
        
        report = self.reporter.generate_streak_report()
        
        assert 'STREAK' in report
        assert 'Habit 1' in report or 'days' in report
    
    def test_progress_bar_creation(self):
        """Test progress bar creation"""
        bar = self.reporter._create_progress_bar(50)
        
        assert '[' in bar
        assert ']' in bar
        assert '█' in bar
        assert '░' in bar
    
    def test_comprehensive_report(self):
        """Test comprehensive report generation"""
        report = self.reporter.generate_comprehensive_report()
        
        assert 'TRADERS MASTERMIND' in report
        assert 'COMPLETE DISCIPLINE REPORT' in report
        assert 'Generated' in report


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
