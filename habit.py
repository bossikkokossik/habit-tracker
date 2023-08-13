from datetime import datetime, timedelta
import json

def generateHabitId(mode, id):
    """
    Generate a unique habit ID based on the given mode and ID.

    :param mode: Mode indicating whether the habit is being added or edited.
    :param id: ID of the habit.
    :return: Generated habit ID as a string.
    """
    if mode == "add":
        data = json.loads(open("./habits.json", "r").read())
        if data == []:
            habit_id = 1
        else:
            habit_id = int(data[-1]["habit_id"]) + 1
        return habit_id
    elif mode == "edit":
        habit_id = id
        return habit_id


class Habit:
    """
    Represents a habit with its details and progress.
    """
    def __init__(self, habit_id, title, description, 
                 frequency, category, significance, 
                 progress_entries, end_date, mode, id="",  
                 next_deadline=None):
        """
        Initialize a Habit object with provided information.

        :param habit_id: ID of the habit.
        :param title: Title of the habit.
        :param description: Description of the habit.
        :param frequency: Frequency of the habit (daily, weekly, monthly).
        :param category: Category of the habit.
        :param significance: Significance level of the habit.
        :param progress_entries: List of progress entries for the habit.
        :param end_date: End date of the habit.
        :param mode: Mode indicating whether the habit is being added or edited.
        :param id: ID of the habit.
        :param next_deadline: Next deadline for the habit.
        """
        self.habit_id = generateHabitId(mode, id)
        self.title = title
        self.description = description
        self.active = True
        self.start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.end_date = end_date
        self.frequency = frequency
        self.successes = 0
        self.current_streak = 0
        self.longest_streak = 0
        self.category = category
        self.significance = significance
        self.next_deadline = next_deadline
        self.progress_entries = progress_entries
        self.days = 0
    
    def complete_habit(self):
        """
        Mark the habit as completed.
        """
        self.active = False
        self.end_date = datetime.now()

    def reset_current_streak(self):
        """
        Reset the current streak of the habit to 0.
        """
        self.current_streak = 0

    def update_longest_streak(self):
        """
        Update the longest streak of the habit based on the current streak.
        """
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak

    def is_completed_today(self) -> bool:
        """
        Check if the habit is completed today by checking the latest progress entry.

        :return: True if the habit is completed today, False otherwise.
        """
        if not self.progress_entries:
            return False
        latest_entry = self.progress_entries[-1]
        return (latest_entry["comment"] 
                and latest_entry["satisfaction_level"] >= 0 
                and datetime.now().date() == latest_entry.get("timestamp", datetime.now()).date())

    def days_remaining(self) -> int:
        """
        Calculate the number of days remaining until the next deadline.

        :return: Number of days remaining or None if there is no next deadline.
        """
        if not self.next_deadline:
            return None
        return (self.next_deadline - datetime.now()).days

    def update_next_deadline(self):
        """
        Update the next deadline for the habit based on its frequency.
        """
        if self.frequency == "daily":
            self.next_deadline = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S.%f")
        elif self.frequency == "weekly":
            self.next_deadline = (datetime.now() + timedelta(weeks=7)).strftime("%Y-%m-%d %H:%M:%S.%f")
        elif self.frequency == "monthly":
            self.next_deadline = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S.%f")
        else:
            raise ValueError(f"Unknown frequency: {self.frequency}")

    def update_success_status(self):
        """
        Update the success status of the habit based on whether it was completed today.
        """
        if self.is_completed_today():
            self.successes += 1
            self.current_streak += 1
        else:
            self.reset_current_streak()
        self.update_longest_streak()