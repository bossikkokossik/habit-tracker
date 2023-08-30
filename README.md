# Habit Tracker

A basic GUI application for tracking daily, weekly, or monthly habits defined by the user.

## Features

- List of all tracked habits
- Adding new habits
- Editing existing habits
- Checking habit details (metrics)
- Displaying general analytics (success rates, top streaks, etc.)
- Clean and intuitive GUI

## Installation

In order to use the application, you first need to install Python 3.11 (or newer) - follow the instructions specified [here](https://wiki.python.org/moin/BeginnersGuide/Download). Then, install the required packages by running the following inside your terminal:

```bash
pip install -r requirements.txt
```
    
## Run

To open the application, simply type the following in your terminal. The application comes with a set of predefined habits.

### Unix
```bash
python3 app.py
```

### Windows
```bash
python app.py
```

## Usage

In order to add new habits, use the `Add habit` button in the left-side menu panel. The adding menu will open, where you will be able to provide a habit name, a description, a goal for the habit, as well as to select a frequency and a category for the habit. As soon as you are done, click the `Save` button to add your habit.

When you complete a habit, select it from the dashboard, and click  the `Mark done` button to update your progress. Similarly, you can edit (or delete) any of your habits by selecting it and clicking the `Edit` button.

In order to view more details about your progress, either select a habit and click the `Metrics` button, if you want the details about a specific habit, or click the `Analytics` button to view the general statistics, and choose the statistic you would like to know.

## Tests

To ensure everything works as expected, you may run the unit test suite with the following command:

### Unix
```bash
python3 -m unittest
```

### Windows
```bash
python -m unittest
```