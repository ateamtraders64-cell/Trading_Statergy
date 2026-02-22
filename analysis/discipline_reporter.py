# Discipline Tracker Reporter & Dashboard

"""
Generate discipline tracking reports and visual dashboards.
Creates reports similar to Traders Mastermind discipline tracker.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List
from analysis.discipline_tracker import DisciplineTracker


class DisciplineReporter:
    """Generate reports and dashboards for discipline tracking"""
    
    def __init__(self, tracker: DisciplineTracker):
        self.tracker = tracker
    
    def generate_daily_report(self, date: str = None) -> str:
        """Generate a single day's discipline report"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        daily_prog = self.tracker.get_daily_progress(date)
        day_name = datetime.strptime(date, '%Y-%m-%d').strftime('%A')
        
        report = f"""
{'='*60}
DAILY DISCIPLINE REPORT - {day_name.upper()} ({date})
{'='*60}

Completion Status: {daily_prog['completed']}/{daily_prog['total']} habits
Completion Rate: {daily_prog['completion_rate']:.1f}%

Status: {self._get_status_emoji(daily_prog['completion_rate'])}

{'='*60}
"""
        return report
    
    def generate_weekly_report(self, start_date: str = None) -> str:
        """Generate weekly discipline report"""
        if start_date is None:
            # Last Monday
            today = datetime.now()
            start_date = (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')
        
        weekly_prog = self.tracker.get_weekly_progress(start_date)
        
        report = f"""
{'='*60}
WEEKLY DISCIPLINE REPORT
Week Starting: {start_date}
{'='*60}

Overall Weekly Progress: {weekly_prog['week_progress']}

Daily Breakdown:
"""
        
        for day_name, day_data in weekly_prog['days'].items():
            bar = self._create_progress_bar(day_data['completion_rate'])
            report += f"\n{day_name}: {bar} {day_data['completion_rate']:.0f}%"
        
        report += f"\n\nAverage Completion Rate: {weekly_prog['average_completion_rate']:.1f}%"
        report += f"\n{'='*60}\n"
        
        return report
    
    def generate_habit_dashboard(self) -> str:
        """Generate dashboard for all daily habits"""
        dashboard = f"""
{'='*70}
DAILY HABITS DISCIPLINE TRACKER
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*70}

OVERALL HABIT PROGRESS: {self._get_overall_progress_emoji()}
"""
        
        overall = self.tracker.get_overall_progress(7)
        overall_pct = overall['overall_progress_percentage']
        dashboard += f"\n{self._create_progress_bar(overall_pct, length=40)} {overall_pct:.1f}%\n"
        
        dashboard += f"\nStatus: {overall['status']}\n"
        dashboard += f"{'='*70}\n\n"
        
        dashboard += "DAILY HABITS\n"
        dashboard += f"{'Habit':<30} {'Progress':<15} {'Goal':<6} {'Days':<4}\n"
        dashboard += "-" * 70 + "\n"
        
        for habit_id, habit in self.tracker.daily_habits.items():
            progress = self.tracker.get_habit_progress(habit_id, 7)
            completion_rate = progress['completion_rate']
            bar = self._create_progress_bar(completion_rate, length=12)
            
            dashboard += f"{habit.emoji} {habit.name:<27} {bar} {completion_rate:>5.0f}%  {habit.goal:>3}  {len(progress['completions']):>3}\n"
        
        dashboard += f"\n{'='*70}\n"
        
        # Category breakdown
        dashboard += "\nCATEGORY ANALYSIS\n"
        categories = set(h.category for h in self.tracker.daily_habits.values())
        
        for category in sorted(categories):
            cat_prog = self.tracker.get_category_progress(category, 7)
            cat_avg = cat_prog['category_average']
            bar = self._create_progress_bar(cat_avg, length=20)
            dashboard += f"\n{category.upper()}: {bar} {cat_avg:.1f}%"
        
        dashboard += f"\n\n{'='*70}\n"
        
        return dashboard
    
    def generate_violations_report(self) -> str:
        """Generate report of habit violations"""
        violations = self.tracker.get_violations(7)
        
        report = f"""
{'='*70}
VIOLATIONS & DISCIPLINE GAPS REPORT
Last 7 Days
{'='*70}

Total Violations: {violations['violation_count']}
Most Common Violation: {violations['most_common_category'] or 'None'}

"""
        
        if violations['violations']:
            report += f"{'Date':<12} {'Habit':<30} {'Category':<15} {'Notes':<20}\n"
            report += "-" * 70 + "\n"
            
            for v in violations['violations']:
                report += f"{v['date']:<12} {v['habit']:<30} {v['category']:<15} {v['notes']:<20}\n"
        else:
            report += "✅ No violations recorded! Excellent discipline!\n"
        
        report += f"\n{'='*70}\n"
        return report
    
    def generate_streak_report(self) -> str:
        """Generate current streaks for all habits"""
        report = f"""
{'='*70}
HABIT STREAKS REPORT
{'='*70}

"""
        
        habit_streaks = []
        for habit_id in self.tracker.daily_habits.keys():
            streak_data = self.tracker.get_streak(habit_id)
            habit_streaks.append(streak_data)
        
        # Sort by streak length (descending)
        habitat_streaks = sorted(habit_streaks, key=lambda x: x['current_streak'], reverse=True)
        
        report += f"{'Habit':<35} {'Streak':<15} {'Status':<15}\n"
        report += "-" * 70 + "\n"
        
        for streak in habitat_streaks:
            streak_display = f"{streak['current_streak']} {'days' if streak['current_streak'] != 1 else 'day'}"
            report += f"{streak['habit_name']:<35} {streak_display:<15} {streak['streak_status']:<15}\n"
        
        report += f"\n{'='*70}\n"
        return report
    
    def generate_monthly_performance(self) -> str:
        """Generate monthly performance summary"""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        # Calculate 30-day average
        all_days = []
        for i in range(30):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            prog = self.tracker.get_daily_progress(date)
            all_days.append(prog['completion_rate'])
        
        avg_completion = sum(all_days) / len(all_days) if all_days else 0
        
        report = f"""
{'='*70}
MONTHLY PERFORMANCE SUMMARY
{start_date} to {end_date}
{'='*70}

30-Day Average Discipline: {self._create_progress_bar(avg_completion, 40)} {avg_completion:.1f}%

Best Day: {max(all_days):.0f}%
Worst Day: {min(all_days):.0f}%
Trend: {"↗️ Improving" if all_days[0] > all_days[-1] else "↘️ Declining" if all_days[0] < all_days[-1] else "→ Stable"}

Daily Consistency: {self._calculate_consistency(all_days):.1f}%

{'='*70}
"""
        return report
    
    def generate_comprehensive_report(self) -> str:
        """Generate complete discipline report with all sections"""
        report = "\n" + "="*70 + "\n"
        report += "TRADERS MASTERMIND - COMPLETE DISCIPLINE REPORT\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "="*70 + "\n\n"
        
        report += self.generate_habit_dashboard()
        report += self.generate_monthly_performance()
        report += self.generate_streak_report()
        report += self.generate_violations_report()
        report += self.generate_weekly_report()
        
        return report
    
    def export_as_json(self, filename: str = None) -> str:
        """Export complete tracking data as JSON"""
        if filename is None:
            filename = f"discipline_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = self.tracker.export_results()
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filename
    
    def export_as_csv(self, filename: str = None) -> str:
        """Export tracking data as CSV for spreadsheet analysis"""
        if filename is None:
            filename = f"discipline_tracking_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        import csv
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            header = ['Date', 'Habit', 'Category', 'Completed', 'Notes']
            writer.writerow(header)
            
            # Data
            for tracking in sorted(self.tracker.tracking, key=lambda x: x.date, reverse=True):
                habit = self.tracker.daily_habits.get(tracking.habit_id)
                if habit:
                    writer.writerow([
                        tracking.date,
                        habit.name,
                        habit.category,
                        'Yes' if tracking.completed else 'No',
                        tracking.notes
                    ])
        
        return filename
    
    # Helper methods
    
    def _create_progress_bar(self, percentage: float, length: int = 20) -> str:
        """Create ASCII progress bar"""
        filled = int(length * percentage / 100)
        bar = '█' * filled + '░' * (length - filled)
        return f"[{bar}]"
    
    def _get_status_emoji(self, percentage: float) -> str:
        """Get emoji status based on percentage"""
        if percentage == 100:
            return "🎯 Perfect!"
        elif percentage >= 90:
            return "🌟 Excellent"
        elif percentage >= 75:
            return "✅ Good"
        elif percentage >= 50:
            return "⚠️ Fair"
        else:
            return "❌ Needs Improvement"
    
    def _get_overall_progress_emoji(self) -> str:
        """Get emoji representation of overall progress"""
        overall = self.tracker.get_overall_progress(7)
        return self._get_status_emoji(overall['overall_progress_percentage'])
    
    def _calculate_consistency(self, values: List[float]) -> float:
        """Calculate consistency score (low variance = high consistency)"""
        if not values or len(values) < 2:
            return 0
        
        import statistics
        avg = statistics.mean(values)
        variance = statistics.variance(values)
        
        # Consistency inversely related to variance (0-100 scale)
        # Higher consistency = values closer to mean
        consistency = max(0, 100 - (variance / 10))
        return min(100, consistency)


# Example CLI usage
def print_dashboard():
    """Print discipline tracker dashboard to console"""
    tracker = DisciplineTracker()
    reporter = DisciplineReporter(tracker)
    
    print(reporter.generate_comprehensive_report())


def print_today():
    """Print today's discipline status"""
    tracker = DisciplineTracker()
    reporter = DisciplineReporter(tracker)
    
    print(reporter.generate_daily_report())


if __name__ == "__main__":
    # Example usage
    print("Discipline Reporter initialized!")
    print("\nTo use:")
    print("  - tracker = DisciplineTracker()")
    print("  - reporter = DisciplineReporter(tracker)")
    print("  - print(reporter.generate_comprehensive_report())")
