from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import List

from habit import Habit

class Analytics:
    """
    Provides various analytical methods for analyzing habits.
    """
    
    def active_habits(self, habits):
        """
        Return a list of active habits from the provided list.

        :param habits: List of Habit objects.
        :return: List of active Habit objects.
        """
        return [habit for habit in habits if habit.active]

    def habits_in_period(self, habits, from_date, to_date):
        """
        Return a list of habits that started within the specified period.

        :param habits: List of Habit objects.
        :param from_date: Start date of the period.
        :param to_date: End date of the period.
        :return: List of Habit objects that started within the period.
        """
        return [habit for habit in habits if from_date <= habit.start_date 
                and habit.start_date <= to_date]

    def top_streak_habit(self, habits):
        """
        Return the habit_id of the habit with the highest streak.

        :param habits: List of Habit objects.
        :return: Habit ID with the highest streak, or None if no habit exists.
        """
        max_streak = max(habits, key=lambda habit: habit.longest_streak)
        return max_streak.habit_id if max_streak else None

    def highest_success_rate(self, habits):
        """
        Return the habit_id of the habit with the highest success rate.

        :param habits: List of Habit objects.
        :return: Habit ID with the highest success rate, or None if no habit exists.
        """
        def success_rate(habit):
            return habit.successes / len(habit.progress_entries) if habit.progress_entries else 0

        success_rate_habit = max(habits, key=success_rate)
        return success_rate_habit.habit_id if success_rate_habit else None

    def highest_failure_rate(self, habits):
        """
        Return the habit_id of the habit with the highest failure rate.

        :param habits: List of Habit objects.
        :return: Habit ID with the highest failure rate, or None if no habit exists.
        """
        def failure_rate(habit):
            habit.start_date = datetime.strptime(habit.start_date, "%Y-%m-%d %H:%M:%S.%f")
            days_since_creation = (datetime.now() - habit.start_date).days
            days_with_progress = len(habit.progress_entries)
            return (days_since_creation - days_with_progress) / days_since_creation if days_since_creation else 0

        failure_rate_habit = max(habits, key=failure_rate)
        return failure_rate_habit.habit_id

    def overall_successes(self, habits):
        """
        Return the total number of successes across all habits.

        :param habits: List of Habit objects.
        :return: Total number of successes.
        """
        return sum(habit.successes for habit in habits)

    def overall_failures(self, habits):
        """
        Return the total number of failures across all habits.

        :param habits: List of Habit objects.
        :return: Total number of failures.
        """
        return sum((datetime.now() - habit.start_date).days - len(habit.progress_entries) for habit in habits)

    def top_category_performance(self, habits):
        """
        Return the category with the highest average success rate.

        :param habits: List of Habit objects.
        :return: Category with the highest average success rate.
        """
        category_success_rates = defaultdict(list)
        for habit in habits:
            category_success_rates[habit.category].append(habit.successes / len(habit.progress_entries) 
                                                          if habit.progress_entries else 0)

        top_category = max(category_success_rates, 
                           key=lambda category: (sum(category_success_rates[category]) 
                                                 / len(category_success_rates[category])))
        return top_category
    
    def top_interval_performance(self, habits):
        """
        Return the interval with the highest average success rate.

        :param habits: List of Habit objects.
        :return: Interval with the highest average success rate.
        """
        interval_success_rates = defaultdict(list)
        for habit in habits:
            interval_success_rates[habit.frequency].append(habit.successes / len(habit.progress_entries) if habit.progress_entries else 0)

        top_interval = max(interval_success_rates, 
                           key=lambda interval: sum(interval_success_rates[interval]) / len(interval_success_rates[interval]))
        return top_interval

    def average_streak_length(self, habits):
        """
        Calculate the average length of the longest streak across all habits.

        :param habits: List of Habit objects.
        :return: Average length of the longest streak.
        """
        return sum(habit.longest_streak for habit in habits) // len(habits)

    def average_streak_break(self, habits):
        """
        Calculate the average number of days between habit creation and the first progress entry.

        :param habits: List of Habit objects.
        :return: Average number of days between creation and first progress entry.
        """
        streak_breaks = []
        for habit in habits:
            habit.start_date = datetime.strptime(str(habit.start_date), 
                                                 "%Y-%m-%d %H:%M:%S.%f")
            streak_breaks.append((datetime.now() - habit.start_date).days - len(habit.progress_entries))
        return sum(streak_breaks) // len(streak_breaks) if streak_breaks else 0

    def average_remaining_time(self, habits):
        """
        Calculate the average remaining time until the next deadline for active habits.

        :param habits: List of Habit objects.
        :return: Average remaining time in days.
        """
        remaining_times = []
        for habit in habits:
            habit.next_deadline = datetime.strptime(habit.next_deadline, 
                                                    "%Y-%m-%d %H:%M:%S.%f")
            if habit.next_deadline:
                remaining_times.append((habit.next_deadline - datetime.now()).days)
        return sum(remaining_times) // len(remaining_times) if remaining_times else 0