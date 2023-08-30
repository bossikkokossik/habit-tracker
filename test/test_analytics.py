import datetime
import unittest

from analytics import Analytics
from habit import Habit

class AnalyticsTestCase(unittest.TestCase):
    def setUp(self):
        self.analytics = Analytics()
        self.habits = [
            Habit("test_habit_1", "", "daily", "test", 1, [], 
                  datetime.date(2030, 7, 20), "add"),
            Habit("test_habit_2", "", "daily", "test", 1, [], 
                  datetime.date(2030, 7, 21), "add"),
            Habit("test_habit_3", "", "daily", "test", 1, [], 
                  datetime.date(2030, 7, 22), "add"),
            Habit("test_habit_4", "", "daily", "test", 1, [], 
                  datetime.date(2030, 7, 23), "add"),
            Habit("test_habit_5", "", "weekly", "test", 1, [], 
                  datetime.date(2030, 7, 24), "add")
        ]

    def test_active_habits(self):
        output = self.analytics.active_habits(self.habits)
        self.assertEqual(len(output), 5)

    def test_habits_with_frequency(self):
        output = self.analytics.habits_with_frequency(self.habits, "daily")
        self.assertEqual(len(output), 4)

    def test_top_streak_habit(self):
        self.habits[1].longest_streak = 5
        output = self.analytics.top_streak_habit(self.habits)
        self.assertEqual(output, self.habits[1].habit_id)

    def test_get_longest_streak(self):
        self.habits[0].complete_habit()
        self.habits[0].update_success_status()
        output = self.analytics.get_longest_streak(self.habits[0])
        self.assertEqual(output, 1)

    def test_habits_in_period(self):
        output = self.analytics.habits_in_period(self.habits, 
                                                 datetime.date(2020, 1, 1), 
                                                 datetime.date(2030, 1, 1))
        self.assertEqual(len(output), 5)

    def test_highest_success_rate(self):
        self.habits[1].complete_habit()
        self.habits[1].update_success_status()
        output = self.analytics.highest_success_rate(self.habits)
        self.assertEqual(output, self.habits[1].habit_id)

    def test_highest_failure_rate(self):
        for i in range(5):
            if i != 1:
                self.habits[i].complete_habit()
                self.habits[i].update_success_status()
        output = self.analytics.highest_failure_rate(self.habits)
        self.assertEqual(output, self.habits[1].habit_id)

    def test_overall_successes(self):
        for i in range(5):
            self.habits[i].complete_habit()
            self.habits[i].update_success_status()
        output = self.analytics.overall_successes(self.habits)
        self.assertEqual(output, 5)

    def test_overall_failures(self):
        self.habits[0].start_date = datetime.date(1969, 7, 20)
        output = self.analytics.overall_failures(self.habits)
        self.assertGreater(output, 3000)
    
    def test_top_category_performance(self):
        self.habits.append(Habit("test_habit_6", "", "daily", "test_alt", 1, [], 
                           datetime.date(2030, 7, 31), "add"))
        self.habits[-1].complete_habit()
        self.habits[-1].update_success_status()
        output = self.analytics.top_category_performance(self.habits)
        self.assertEqual(output, "test_alt")

    def test_top_frequency_performance(self):
        self.habits.append(Habit("test_habit_6", "", "monthly", "test_alt", 1, [], 
                           datetime.date(2030, 7, 31), "add"))
        self.habits[-1].complete_habit()
        self.habits[-1].update_success_status()
        output = self.analytics.top_frequency_performance(self.habits)
        self.assertEqual(output, "monthly")

    def test_average_streak_length(self):
        self.habits[0].complete_habit()
        self.habits[0].update_success_status()
        output = self.analytics.average_streak_length(self.habits)
        self.assertEqual(output, 0.2)

    def test_average_streak_break(self):
        self.habits[0].start_date = datetime.date(1969, 7, 20)
        output = self.analytics.average_streak_break(self.habits)
        self.assertGreater(output, 3000)

    def test_average_remaining_time(self):
        output = self.analytics.average_remaining_time(self.habits)
        self.assertEqual(output, 0)

if __name__ == "__main__":
    unittest.main()