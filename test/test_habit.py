import datetime
import unittest

from habit import Habit

class HabitTestCase(unittest.TestCase):
    def setUp(self):
        self.habit = Habit("test_habit", "", "daily", "test", 1, [], 
                           datetime.date(2030, 7, 20).strftime("%Y-%m-%d %H:%M:%S"), "add")

    def test_complete_habit(self):
        self.habit.complete_habit()
        self.assertEqual(self.habit.progress_entries[-1]["timestamp"].date(), 
                         datetime.datetime.now().date())
        
    def test_reset_current_streak(self):
        self.habit.current_streak = 5
        self.habit.reset_current_streak()
        self.assertEqual(self.habit.current_streak, 0)

    def test_update_longest_streak(self):
        self.habit.current_streak = self.habit.longest_streak + 5
        self.habit.update_longest_streak()
        self.assertGreaterEqual(self.habit.longest_streak, self.habit.current_streak)

    def test_is_completed_today(self):
        today_habit = Habit("completed_today", "", "daily", "test", 1, [],
                            datetime.date(2030, 7, 20).strftime("%Y-%m-%d %H:%M:%S"), "add")
        today_habit.complete_habit()
        self.assertTrue(not self.habit.is_completed_today() and today_habit.is_completed_today())

    def test_days_remaining(self):
        delta = datetime.timedelta(days=50)
        default_days = self.habit.days_remaining()
        self.habit.next_deadline = datetime.datetime.now() + delta
        days = self.habit.days_remaining()
        self.assertTrue(default_days == None and days + 1 == delta.days)

    def test_update_next_deadline(self):
        self.habit.update_next_deadline()
        self.assertEqual(datetime.datetime.fromisoformat(self.habit.next_deadline).date(), 
                         (datetime.datetime.now() + datetime.timedelta(days=1)).date())

    def test_update_success_status(self):
        successes = 5
        streak = 5

        self.habit.successes = successes
        self.habit.current_streak = streak

        today_habit = Habit("completed_today", "", "daily", "test", 1, 
                            [{"comment": "test", "timestamp": datetime.datetime.now()}], 
                            datetime.date(2030, 7, 20).strftime("%Y-%m-%d %H:%M:%S"), "add")
        today_habit.successes = successes
        today_habit.current_streak = streak
        
        self.habit.update_success_status()
        def_successes = self.habit.successes
        def_streak = self.habit.current_streak

        today_habit.update_success_status()
        tod_successes = today_habit.successes
        tod_streak = today_habit.current_streak

        self.assertTrue(def_successes == successes
                        and def_streak == 0
                        and tod_successes == successes + 1
                        and tod_streak == streak + 1)
        
if __name__ == "__main__":
    unittest.main()