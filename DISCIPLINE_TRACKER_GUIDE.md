# Discipline Tracker - User Guide

**Trading Discipline Tracker**  
*Track daily trading habits and measure rule adherence*

---

## Overview

The Discipline Tracker helps you build consistent trading habits by:
- ✅ Tracking daily discipline habits
- 📊 Measuring compliance with trading rules
- 🎯 Setting and monitoring goals
- 📈 Identifying patterns in violations
- 🔥 Building streaks of good discipline

Based on the **Traders Mastermind** discipline tracking model.

---

## Quick Start

### 1. Initialize the Tracker

```python
from analysis.discipline_tracker import DisciplineTracker
from analysis.discipline_reporter import DisciplineReporter

# Load configuration
tracker = DisciplineTracker()
reporter = DisciplineReporter(tracker)
```

### 2. Track Habits Each Day

```python
from datetime import datetime

today = datetime.now().strftime('%Y-%m-%d')

# Mark habits as complete
tracker.mark_habit_complete(today, 'check_economic_calendar', notes='Checked EUR/USD events')
tracker.mark_habit_complete(today, 'higher_timeframe_analysis')

# Mark habits as incomplete (with reason)
tracker.mark_habit_incomplete(today, 'journal_trades', notes='Ran out of time')
```

### 3. Generate Reports

```python
# Print today's status
print(reporter.generate_daily_report())

# Print weekly summary
print(reporter.generate_weekly_report())

# Print full dashboard
print(reporter.generate_comprehensive_report())

# Export to files
reporter.export_as_json()
reporter.export_as_csv()
```

---

## Features

### 📅 Daily Habits (15 Built-in)

Based on the Traders Mastermind template, includes:

**Preparation & Planning**
- ✅ Check Economic Calendar - Review upcoming economic events
- ✅ Higher Timeframe Analysis - Confirm trends on larger timeframes
- ✅ Draw On Key Levels - Mark support/resistance levels
- ✅ Review Major Markets - Check overall market movements

**Risk Management**
- ✅ No Trades First 5 Mins - Wait after market open
- ✅ Always Enter A Stop - Never trade without stop loss
- ✅ Stick To Daily Risk Rules - Maintain daily loss limits
- ✅ 5 Trades Per Day Max - Don't over trade

**Trade Execution**
- ✅ Only Planned Trades - Follow your plan
- ✅ Calculate RVR - Check risk-reward before entry
- ✅ Check Sentiment - Assess market sentiment
- ✅ Mark Intraday Charts - Prepare charts beforehand

**Psychology & Discipline**
- ✅ No Meddling With Trades - Don't adjust stops
- ✅ Take Walk At Lunch - Step away from screens
- ✅ Check Sentiment - Avoid emotional decisions

**Review & Analysis**
- ✅ Journal Trades - Document each trade

### 📆 Weekly Habits (8 Built-in)

- ✅ Review All Trades - Comprehensive weekly review
- ✅ Analyse Charts - Deep price action analysis
- ✅ Watch Trading Videos - Educational content
- ✅ Write Weekly Goals - Plan the week ahead
- ✅ Read Trading Book - Continue learning
- ✅ Analyse Losses - Learn from mistakes
- ✅ Plan New Setups - Identify new opportunities
- ✅ Relax and Unwind - Manage trading stress

### 📊 Metrics Tracked

**Daily**
- Completion rate (%)
- Habits completed vs total
- Category performance
- Rule violations

**Weekly**
- Average completion rate
- Day-by-day breakdown
- Weekly average progress
- Trend analysis

**Overall**
- 7-day discipline average
- Current streaks (per habit)
- Violation patterns
- Progress consistency

---

## Categories

Habits are organized by category for focused analysis:

| Category | Color | Importance | Purpose |
|----------|-------|------------|---------|
| **Risk Management** | 🔴 Red | Critical | Protect capital |
| **Preparation** | 🟢 Green | High | Plan trades |
| **Execution** | 🔵 Blue | High | Execute trades |
| **Psychology** | 🟠 Orange | High | Maintain discipline |
| **Review** | 🟣 Purple | Medium | Learn & improve |

---

## Usage Examples

### Example 1: Track Your Day

```python
tracker = DisciplineTracker()
today = datetime.now().strftime('%Y-%m-%d')

# Morning prep
tracker.mark_habit_complete(today, 'check_economic_calendar')
tracker.mark_habit_complete(today, 'higher_timeframe_analysis')

# During trading
tracker.mark_habit_complete(today, 'always_enter_stop')
tracker.mark_habit_complete(today, 'no_trades_first_5_mins')

# Trading went well - mark accordingly
tracker.mark_habit_complete(today, 'stick_to_risk_rules')

# One habit missed
tracker.mark_habit_incomplete(today, 'journal_trades', notes='Will journal tonight')

# Check results
progress = tracker.get_daily_progress(today)
print(f"Today: {progress['completed']}/{progress['total']} ({progress['completion_rate']:.0f}%)")
```

### Example 2: Weekly Review

```python
# Get last 7 days of data
weekly = tracker.get_weekly_progress(start_date)
print(f"Week average: {weekly['average_completion_rate']:.1f}%")

# Check violations
violations = tracker.get_violations(7)
print(f"Violations this week: {violations['violation_count']}")
print(f"Most common: {violations['most_common_category']}")

# Check streaks
for habit_id in tracker.daily_habits.keys():
    streak = tracker.get_streak(habit_id)
    if streak['current_streak'] >= 3:
        print(f"🔥 {streak['habit_name']}: {streak['current_streak']} day streak!")
```

### Example 3: Add Custom Habits

```python
# Add a custom habit
tracker.add_custom_habit(
    id='my_custom_habit',
    name='My Custom Rule',
    description='A trading rule I want to track',
    emoji='🎯',
    goal=15,
    category='risk',
    importance=5
)

# Now track it
tracker.mark_habit_complete(today, 'my_custom_habit')
```

### Example 4: Generate Full Dashboard

```python
reporter = DisciplineReporter(tracker)

# Print beautiful dashboard
print(reporter.generate_comprehensive_report())

# Export for spreadsheet analysis
reporter.export_as_csv('my_discipline_data.csv')
reporter.export_as_json('my_discipline_data.json')
```

---

## Configuration

Edit `config/discipline_goals.json` to:
- Add/remove daily habits
- Add/remove weekly habits
- Change goals
- Set monthly targets
- Customize categories

**Example: Add a new daily habit**

```json
{
  "id": "my_new_habit",
  "name": "My New Habit",
  "description": "What this habit is about",
  "emoji": "🎯",
  "goal": 15,
  "category": "risk",
  "importance": 4
}
```

---

## Metrics & Reports

### Overall Progress Percentage

Shows your overall discipline score (0-100%)
- 90%+ = 🌟 Excellent
- 75-89% = ✅ Good
- 50-74% = ⚠️ Fair
- Below 50% = ❌ Needs Improvement

### Daily Progress

How many habits you completed each day.

### Habit Streaks

Consecutive days completing a habit.
- 3+ days = 🔥 Hot streak!
- Building momentum towards goals

### Violations Report

Tracks incomplete habits and reasons.
- Identify patterns
- Recognize blockers
- Target improvements

### Category Analysis

Performance by habit category:
- Risk Management
- Preparation
- Execution
- Psychology
- Review

---

## Best Practices

### 1. **Track Consistently**
- Update tracker daily as you complete habits
- Add notes for incomplete habits
- Don't skip days

### 2. **Review Weekly**
- Review your week every Sunday
- Identify patterns in violations
- Celebrate streaks and improvements

### 3. **Monthly Assessment**
- Generate comprehensive monthly report
- Analyze trends
- Adjust goals if needed

### 4. **Use Feedback**
- Most violated categories? Focus there.
- Strong streaks? Maintain them.
- Consistency low? Reduce daily habits temporarily.

### 5. **Adapt Habits**
- Add habits that matter for YOUR trading
- Remove habits that don't apply
- Keep between 10-15 active daily habits

---

## API Reference

### DisciplineTracker Class

```python
# Initialization
tracker = DisciplineTracker(config_file='config/discipline_goals.json')

# Mark habits
tracker.mark_habit_complete(date, habit_id, notes='')
tracker.mark_habit_incomplete(date, habit_id, notes='')

# Get metrics
tracker.get_daily_progress(date)
tracker.get_weekly_progress(start_date)
tracker.get_overall_progress(days=7)
tracker.get_habit_progress(habit_id, days=7)
tracker.get_category_progress(category, days=7)
tracker.get_violations(days=7)
tracker.get_streak(habit_id)

# Custom habits
tracker.add_custom_habit(id, name, description, emoji, goal, category, importance)

# Export
tracker.export_results()
```

### DisciplineReporter Class

```python
reporter = DisciplineReporter(tracker)

# Reports
reporter.generate_daily_report(date)
reporter.generate_weekly_report(start_date)
reporter.generate_habit_dashboard()
reporter.generate_violations_report()
reporter.generate_streak_report()
reporter.generate_monthly_performance()
reporter.generate_comprehensive_report()

# Export
reporter.export_as_json(filename)
reporter.export_as_csv(filename)
```

---

## Integration with Trading

Use discipline tracking alongside your strategy:

```python
from strategies.base import Strategy
from analysis.discipline_tracker import DisciplineTracker

class DisciplinedStrategy(Strategy):
    def __init__(self, parameters):
        super().__init__(name='DisciplinedStrategy', parameters=parameters)
        self.discipline = DisciplineTracker()
    
    def execute_trade(self, signal):
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Check risk rule
        if self.check_risk_rules():
            self.discipline.mark_habit_complete(today, 'stick_to_risk_rules')
        else:
            self.discipline.mark_habit_incomplete(today, 'stick_to_risk_rules')
        
        # Execute if discipline allows
        if self.discipline.get_daily_progress(today)['completion_rate'] > 50:
            return super().execute_trade(signal)
```

---

## Troubleshooting

**Q: Habits not loading from config?**
A: Check that `config/discipline_goals.json` exists and is valid JSON.

**Q: Reports not showing data?**
A: Make sure you've tracked at least one habit using `mark_habit_complete()`.

**Q: Want to start fresh?**
A: Delete the tracking records or create new DisciplineTracker instance.

**Q: How to export for Excel?**
A: Use `reporter.export_as_csv()` and open in Excel/Sheets.

---

## Tips for Success

1. **Start Simple**: Begin with 5-10 most important habits
2. **Track Daily**: Make it a routine (morning/evening)
3. **Review Weekly**: Assess what worked and what didn't
4. **Celebrate Wins**: Notice your streaks and improvements
5. **Be Realistic**: Adjust goals based on actual capacity
6. **Adapt**: Add/remove habits as your trading evolves
7. **Learn**: Use violations to identify your weaknesses

---

## Integration Checklist

- [x] Daily habit tracking
- [x] Weekly habit tracking
- [x] Progress reporting
- [x] Streak calculation
- [x] Violation tracking
- [x] Category analysis
- [x] JSON/CSV export
- [x] Comprehensive dashboards

---

**Start tracking your discipline today and build consistent trading habits!** 🚀

For more details, see:
- [DisciplineTracker code](analysis/discipline_tracker.py)
- [DisciplineReporter code](analysis/discipline_reporter.py)
- [Configuration file](config/discipline_goals.json)
- [Test examples](tests/test_discipline_tracker.py)
