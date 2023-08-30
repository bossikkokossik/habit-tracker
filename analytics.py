from __future__ import annotations

from collections import defaultdict
from datetime import datetime

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
    
    def habits_with_frequency(self, habits, frequency):
        """
        Return a list of habits with the given frequency.

        :param habits: List of Habit objects.
        :param frequency: The frequency of Habit objects to be returned.
        :return: List of Habit objects with given frequency.
        """
        return [habit for habit in habits if habit.frequency == frequency]
    
    def top_streak_habit(self, habits):
        """
        Return the habit_id of the habit with the highest streak.

        :param habits: List of Habit objects.
        :return: Habit ID with the highest streak, or None if no habit exists.
        """
        max_streak = max(habits, key=lambda habit: habit.longest_streak)
        return max_streak.habit_id if max_streak else None
    
    def get_longest_streak(self, habit):
        """
        Return the longest run streak of the given habit.

        :param habit: The habit to get the longest streak of.
        :return: The longest streak of the given habit.
        """
        return habit.longest_streak

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

    def highest_success_rate(self, habits):
        """
        Return the habit_id of the habit with the highest success rate.

        :param habits: List of Habit objects.
        :return: Habit ID with the highest success rate, or None if no habit exists.
        """
        def success_rate(habit):
            days_since_creation = (datetime.now().date() - habit.start_date).days + 1
            if habit.frequency == "weekly":
                days_since_creation = datetime.now().date().isocalendar()[1] - habit.start_date.isocalendar()[1] + 1
            elif habit.frequency == "monthly":
                days_since_creation = ((datetime.now().date().year - habit.start_date.year) * 12 
                                        + (datetime.now().date().month - habit.start_date.month) - 1 - len(habit.progress_entries)) + 1
            days_with_progress = len(habit.progress_entries)
            return days_with_progress / days_since_creation if days_since_creation else 0

        success_rate_habit = max(habits, key=success_rate)
        return success_rate_habit.habit_id if success_rate_habit else None

    def highest_failure_rate(self, habits):
        """
        Return the habit_id of the habit with the highest failure rate.

        :param habits: List of Habit objects.
        :return: Habit ID with the highest failure rate, or None if no habit exists.
        """
        def failure_rate(habit):
            days_since_creation = (datetime.now().date() - habit.start_date).days + 1
            if habit.frequency == "weekly":
                days_since_creation = datetime.now().date().isocalendar()[1] - habit.start_date.isocalendar()[1] + 1
            elif habit.frequency == "monthly":
                days_since_creation = ((datetime.now().date().year - habit.start_date.year) * 12 
                                        + (datetime.now().date().month - habit.start_date.month) - len(habit.progress_entries)) + 1
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
        total_failures = 0
        for habit in habits:
            if habit.frequency == "daily":
                total_failures += (datetime.now().date() - habit.start_date).days - len(habit.progress_entries)
            elif habit.frequency == "weekly":
                total_failures += datetime.now().date().isocalendar()[1] - habit.start_date.isocalendar()[1] - len(habit.progress_entries)
            else:
                total_failures += ((datetime.now().date().year - habit.start_date.year) * 12 
                                     + (datetime.now().date().month - habit.start_date.month) - 1 - len(habit.progress_entries))
        return total_failures if total_failures >= 0 else 0

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
    
    def top_frequency_performance(self, habits):
        """
        Return the interval with the highest average success rate.

        :param habits: List of Habit objects.
        :return: Interval with the highest average success rate.
        """
        frequency_success_rates = defaultdict(list)
        for habit in habits:
            frequency_success_rates[habit.frequency].append(habit.successes / len(habit.progress_entries) if habit.progress_entries else 0)

        top_frequency = max(frequency_success_rates, 
                           key=lambda interval: sum(frequency_success_rates[interval]) / len(frequency_success_rates[interval]))
        return top_frequency

    def average_streak_length(self, habits):
        """
        Calculate the average length of the longest streak across all habits.

        :param habits: List of Habit objects.
        :return: Average length of the longest streak.
        """
        return sum(habit.longest_streak for habit in habits) / len(habits)

    def average_streak_break(self, habits):
        """
        Calculate the average number of days between habit creation and the first progress entry.

        :param habits: List of Habit objects.
        :return: Average number of days between creation and first progress entry.
        """
        streak_breaks = []
        for habit in habits:
            if habit.frequency == "daily":
                streak_breaks.append((datetime.now().date() - habit.start_date).days - len(habit.progress_entries))
            elif habit.frequency == "weekly":
                streak_breaks.append(datetime.now().date().isocalendar()[1] - habit.start_date.isocalendar()[1] - len(habit.progress_entries))
            else:
                streak_breaks.append((datetime.now().date().year - habit.start_date.year) * 12 
                                     + (datetime.now().date().month - habit.start_date.month) - 1 - len(habit.progress_entries))
        total_breaks = sum(streak_breaks)
        return total_breaks / len(streak_breaks) if streak_breaks else 0

    def average_remaining_time(self, habits):
        """
        Calculate the average remaining time until the next deadline for active habits.

        :param habits: List of Habit objects.
        :return: Average remaining time in days.
        """
        remaining_times = []
        for habit in habits:
            if habit.next_deadline:
                habit.next_deadline = datetime.strptime(habit.next_deadline, 
                                                        "%Y-%m-%d %H:%M:%S")
                remaining_times.append((habit.next_deadline - datetime.now()).days)
        return sum(remaining_times) / len(remaining_times) if remaining_times else 0