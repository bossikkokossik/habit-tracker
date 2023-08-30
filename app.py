from datetime import datetime
from functools import partial
import json

import customtkinter
from tkcalendar import DateEntry
import tkinter
from tkinter import ttk
from tkinter.messagebox import showinfo

from analytics import Analytics
from habit import Habit

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):

    def __init__(self):
        """
        Initialize the Habit Tracker App GUI.

        Sets up the UI components and initializes various attributes.
        """
        super().__init__()

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#242424", 
                fieldbackground="#242424", foreground="white")
        
        self.dialog_habbit_number = ""
        self.lists = list() 
        self.id = 0
        self.selected_value = []
        self.datas = []
        self.infos = []
        self.title("Habit Tracker App")
        self.geometry("1000x600")

        # Main container
        self.main_container = customtkinter.CTkFrame(self, corner_radius=10)
        self.main_container.pack(fill=tkinter.BOTH, expand=True, 
                                 padx=10, pady=10)
        
        # Menu
        self.left_side_panel = customtkinter.CTkFrame(self.main_container, 
                                                      width=100, corner_radius=10)
        self.left_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, 
                                  expand=False, padx=5, pady=5)
        self.left_side_panel.grid_columnconfigure(0, weight=1)
        self.left_side_panel.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=0)
        self.left_side_panel.grid_rowconfigure((6), weight=1)
        self.logo_label = customtkinter.CTkLabel(self.left_side_panel, 
                                                 text="Welcome! \n", 
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
    
        # UI scaling
        self.scaling_label = customtkinter.CTkLabel(self.left_side_panel, 
                                                    text="UI Scaling:", 
                                                    anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.left_side_panel, 
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20), sticky="s")
    
        # Menu buttons
        self.bt_quit = customtkinter.CTkButton(self.left_side_panel, 
                                               text="Quit", fg_color='#EA0000', 
                                               hover_color='#B20000', 
                                               command=self.close_window)
        self.bt_quit.grid(row=9, column=0, padx=20, pady=10)
        self.bt_edit = customtkinter.CTkButton(self.left_side_panel, 
                                               text="Add Habit", 
                                               command=self.add_habit_func)
        self.bt_edit.grid(row=1, column=0, padx=20, pady=10)
        self.bt_mark_done = customtkinter.CTkButton(self.left_side_panel, 
                                                    text="Mark Done", 
                                                    command=self.mark_done_func)
        self.bt_mark_done.grid(row=2, column=0, padx=20, pady=10)
        self.bt_add_habit = customtkinter.CTkButton(self.left_side_panel, 
                                                    text="Edit", 
                                                    command=self.edit_func, 
                                                    state="disabled")
        self.bt_add_habit.grid(row=3, column=0, padx=20, pady=10)
        self.bt_metrics = customtkinter.CTkButton(self.left_side_panel, 
                                                  text="Metrics", 
                                                  command=self.metrics_func, 
                                                  state="disabled")
        self.bt_metrics.grid(row=4, column=0, padx=20, pady=10)
        self.bt_analytics = customtkinter.CTkButton(self.left_side_panel, 
                                                   text="Analytics", 
                                                   command=self.analytics_func)
        self.bt_analytics.grid(row=5, column=0, padx=20, pady=10)
        self.bt_dash = customtkinter.CTkButton(self.left_side_panel, 
                                               text="Dashboard", 
                                               command=self.dash_func)
        self.bt_dash.grid(row=6, column=0, padx=20, pady=10)
    

        # Right-side panel (dashboard)
        self.right_side_panel = customtkinter.CTkFrame(self.main_container, 
                                                       corner_radius=10, 
                                                       fg_color="#000811")
        self.right_side_panel.pack(side="left", fill=tkinter.BOTH, 
                                   expand=True, padx=5, pady=5)
        self.right_dashboard = customtkinter.CTkFrame(self.main_container, 
                                                      corner_radius=10, 
                                                      fg_color="#000811")
        self.right_dashboard.pack(in_=self.right_side_panel, side=tkinter.TOP, 
                                  fill=tkinter.BOTH, expand=True, padx=0, pady=0)
        self.dash_func()
        
    def dash_func(self):
        """
        Initialize and display the dashboard view.

        Sets up the dashboard UI with a Treeview widget to display habit information.
        Populates the Treeview with data from the 'habits.json' file.
        Binds functions to Treeview events for handling user interactions.
        """
        self.bt_mark_done.configure(state="disabled")
        self.bt_add_habit.configure(state="disabled")
        self.bt_metrics.configure(state="disabled")
        global lists
        self.clear_frame()
        self.title("Dashboard - Habit tracking app")
        
        cols = [
            "Habit", 
            "Description",
            "Category",
            "Frequency", 
            "Last Done", 
            "Current Streak", 
            "Progress"
        ]
        treescroll = ttk.Scrollbar(self.right_dashboard,)
        treescroll.pack(side="right", fill="y")
        treeview = ttk.Treeview(self.right_dashboard,show="headings", 
                                yscrollcommand=treescroll.set, 
                                columns=cols, 
                                height=13)
        treeview.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        treescroll.config(command=treeview.yview)
         
        treeview.column("Habit", width=100)
        treeview.column("Description", width=180)
        treeview.column("Category", width=100)
        treeview.column("Frequency", width=80)
        treeview.column("Last Done", width=100)
        treeview.column("Current Streak", width=100)
        treeview.column("Progress", width=80)
        
        treeview.heading("Habit", text="Habit")
        treeview.heading("Description", text="Description")
        treeview.heading("Category", text="Category")
        treeview.heading("Frequency", text="Frequency")
        treeview.heading("Last Done", text="Last Done")
        treeview.heading("Current Streak", text="Current Streak")
        treeview.heading("Progress", text="Progress")
        self.loaded_data = self.load_data("habits.json")
        self.lists += self.loaded_data
        count = 1
        for record in self.loaded_data:
            if datetime.now() > datetime.fromisoformat(record["next_deadline"]):
                record["current_streak"] = 0
            lists = [
                record["title"], 
                record["description"],
                record["category"],
                record["frequency"], 
                datetime.fromisoformat(record["progress_entries"][-1]["timestamp"]).date() if record["progress_entries"] else "-", 
                record["current_streak"], 
                "{}/{}".format(record["successes"],record["goal"])
            ]
            treeview.insert(parent="", index=tkinter.END, iid=count, text="", values=lists)
            count += 1

        def item_selected(_):
            for selected_item in treeview.selection():
                self.dialog_habbit_number = selected_item
                item = treeview.item(selected_item)
                self.datas = item['values']
                for i in self.loaded_data:
                    if i["title"] == self.datas[0]:
                        pass
                    else: 
                        continue

        def on_tree_click(event):
            item_id = treeview.identify_row(event.y)
            button_id = treeview.identify_column(event.x)
            try:
                selected_val = self.loaded_data[int(item_id)-1]
                if selected_val["progress_entries"]:
                    last_done = datetime.fromisoformat(selected_val["progress_entries"][-1]["timestamp"]).date()
                    if last_done == datetime.now().date():
                        self.bt_mark_done.configure(state="disabled")
                    elif (selected_val["frequency"] == "weekly" 
                        and last_done.isocalendar()[1] == datetime.now().isocalendar()[1] 
                        and last_done.year == datetime.now().year):
                        self.bt_mark_done.configure(state="disabled")
                    elif (selected_val["frequency"] == "monthly" 
                        and last_done.month == datetime.now().month
                        and last_done.year == datetime.now().year):
                        self.bt_mark_done.configure(state="disabled")
                    else:
                        self.bt_mark_done.configure(state="normal")
                else:
                    self.bt_mark_done.configure(state="normal")
                self.bt_add_habit.configure(state="normal")
                self.bt_metrics.configure(state="normal")
            except Exception as e:
                pass

        treeview.bind("<Button-1>", on_tree_click)
        treeview.bind('<<TreeviewSelect>>', item_selected)

    def save_data(self,data, filename):
        """
        Save data to a JSON file.

        Args:
            data (dict): Data to be saved.
            filename (str): Name of the JSON file to save the data to.
        """
        with open(filename, 'w') as file:
            json.dump(data, file, default=str)

    def load_data(self,filename):
        """
        Load data from a JSON file.

        Args:
            filename (str): Name of the JSON file to load data from.

        Returns:
            list: Loaded data as a list.
        """
        try:
            with open(filename, 'r') as file:
                data = json.loads(file.read())
                return data
        except Exception as e:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("[\n]")
                return []
    
    def adding_func(self):
        """
        Add a new habit and update the data.
        This function creates a new Habit instance and updates the data accordingly.
        """
        data = json.loads(open("./habits.json", "r").read())
        category = self.category_entry.get()
        significance = self.goal_entry.get()
        habit_id = self.id + 1
        self.id = habit_id    
        frequency = self.combobox.get()
        title = self.habit_name_entry.get()
        description = self.habit_description_entry.get()
        progress_entries = []
        last_done = ["Have not been marked down"]
        
        habits = Habit(title, description, frequency, category, 
                             significance, progress_entries, last_done, "add")
        habits.update_next_deadline()
        habits.goal = int(significance)
        data.append({
            "habit_id": habit_id, 
            "title": habits.title,
            "description": habits.description,
            "active": habits.active,
            "start_date": habits.start_date,
            "last_done": habits.last_done,
            "frequency": habits.frequency,
            "successes": habits.successes,
            "current_streak": habits.current_streak,
            "longest_streak": habits.longest_streak,
            "category": habits.category,
            "significance": habits.significance,
            "next_deadline": habits.next_deadline,
            "progress_entries": habits.progress_entries,
            "goal": habits.goal
        })
        self.save_data(data, "habits.json")
        self.dash_func()
    
    def adding_func_edit(self, mode, id, progess_entries):
        """
        Edit an existing habit and update the data.

        This function edits an existing Habit instance and updates the data accordingly.

        Args:
            mode (str): The edit mode ("edit").
            id (str): The habit ID.
            progress_entries (list): The progress entries for the habit.
        """
        category = self.category_entry.get()
        significance = self.goal_entry.get()
        habit_id = id
        self.id = habit_id    
        self.dialog_habbit_number = ""
        frequency = self.combobox.get()
        title = self.habit_name_entry.get()
        description = self.habit_description_entry.get()
        progress_entries = progess_entries
        last_done = ["Have not been marked down"]

        habits = Habit(title, description, frequency, category,
                       significance, progress_entries, last_done, mode, id)
        habits.update_next_deadline()
        habits.goal = int(significance)

        self.selected_value_list[int(self.id)-1]["habit_id"] = habit_id
        self.selected_value_list[int(self.id)-1]["title"] = title
        self.selected_value_list[int(self.id)-1]["description"] = description
        self.selected_value_list[int(self.id)-1]["frequency"] = frequency
        self.selected_value_list[int(self.id)-1]["category"] = category
        self.selected_value_list[int(self.id)-1]["significance"] = significance
        self.selected_value_list[int(self.id)-1]["progress_entries"] = progress_entries
        self.selected_value_list[int(self.id)-1]["last_done"] = last_done
                           
        self.save_data(self.selected_value_list, "habits.json")
        self.dash_func()

    def delete_func(self, item_id):
        """
        Delete a habit and update the data.

        This function deletes a habit based on the given itemId and updates the data accordingly.

        Args:
            itemId (str): The ID of the habit to be deleted.
        """
        self.dialog_habbit_number = ""
        data = self.load_data("./habits.json")
        for index, item in enumerate(data):
             if int(item["habit_id"]) > int(item_id)-1:
                 data[index]["habit_id"] = str(int(data[index]["habit_id"]) - 1)   
        del data[int(item_id) - 1]
        self.save_data(data, "./habits.json")
        self.dash_func()
           
    def save_changes(self, mode, id="", progess_entries=[]):
        """
        Save changes made to a habit.

        This function saves changes made to an existing habit by calling the adding_func_edit method.

        Args:
            mode (str): The edit mode ("edit").
            id (str): The habit ID.
            progress_entries (list): The progress entries for the habit.
        """
        self.adding_func_edit(mode, id, progess_entries)

    def add_habit_func(self):
        """
        Open the add habit page for creating a new habit.

        This function sets up the UI for adding a new habit, allowing the user to input details and save the habit.
        """
        self.clear_frame()
        
        self.right_left_side_panel = customtkinter.CTkFrame(self.right_dashboard, 
                                                            width=80, 
                                                            corner_radius=10)
        self.right_left_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, 
                                        expand=False, padx=5, pady=5)
        self.right_left_side_panel.grid_columnconfigure(0, weight=1)
        self.right_left_side_panel.grid_rowconfigure((0, 1, 2, 3), weight=0)
        self.right_left_side_panel.grid_rowconfigure((4, 5), weight=1)
        
        self.goal_label = customtkinter.CTkLabel(self.right_left_side_panel, 
                                                      text="Add Habit Page! \n", 
                                                      font=customtkinter.CTkFont(size=20, weight="bold"))
        self.goal_label.grid(row=1, column=0, padx=20, pady=(20, 10))
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Save", command=self.adding_func)
        self.bt_save.grid(row=2, column=0, padx=20, pady=(100, 0))
        def optionmenu_callback(choice):
            return choice
        self.combobox = customtkinter.CTkOptionMenu(master=self.right_left_side_panel,
                                                    values=["daily", "weekly", "monthly"],
                                                    command=optionmenu_callback)
        self.combobox.grid(row=3, column=0, padx=20, pady=(10,0))
        self.combobox.set("Select frequency")
        self.bt_cancel = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                                 text="Cancel", 
                                                 command=self.dash_func)
        self.bt_cancel.grid(row=4, column=0, padx=20, pady=(200, 0))
        
        self.right_right_side_panel = customtkinter.CTkFrame(self.right_dashboard, 
                                                             width=580, 
                                                             corner_radius=10)
        self.right_right_side_panel.pack(side=tkinter.LEFT, fill=tkinter.BOTH, 
                                         expand=True, padx=5, pady=5)
        
        self.habit_name_label = customtkinter.CTkLabel(self.right_right_side_panel, 
                                                       text="Habit name", 
                                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        self.habit_name_label.pack(pady=(25, 0))
        self.habit_name_entry = customtkinter.CTkEntry(master=self.right_right_side_panel, 
                                                       corner_radius=10, 
                                                       fg_color="black", 
                                                       width=550, 
                                                       height=50)
        self.habit_name_entry.pack(padx=0, pady=20)
        self.logo_label = customtkinter.CTkLabel(self.right_right_side_panel, 
                                                 text="Habit description", 
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.pack()
        self.habit_description_entry = customtkinter.CTkEntry(master=self.right_right_side_panel, 
                                                              corner_radius=10, 
                                                              fg_color="black", 
                                                              width=550, 
                                                              height=50)
        self.habit_description_entry.pack(padx=0, pady=20)
        self.category_label = customtkinter.CTkLabel(self.right_right_side_panel, 
                                                text="Category (change according to your needs)", 
                                                font=customtkinter.CTkFont(size=20, weight="bold"))
        self.category_label.pack()
        self.category_entry = customtkinter.CTkEntry(master=self.right_right_side_panel, 
                                                     corner_radius=10, 
                                                     fg_color="black", 
                                                     width=550, 
                                                     height=50)
        self.category_entry.insert(0, "personal")
        self.category_entry.pack(padx=0, pady=20)
        self.goal_label = customtkinter.CTkLabel(self.right_right_side_panel, 
                                                text="Goal (how many times to complete)", 
                                                font=customtkinter.CTkFont(size=20, weight="bold"))
        self.goal_label.pack()
        self.goal_entry = customtkinter.CTkEntry(master=self.right_right_side_panel, 
                                                 corner_radius=10, 
                                                 fg_color="black", 
                                                 width=550, 
                                                 height=50)
        self.goal_entry.pack(padx=0, pady=20)
        
    def mark_done_func(self):
        """
        Mark a habit as done for the current date.

        This function updates the progress and streak information for a habit when it is marked as done for the current date.
        """
        loaded_data = self.load_data("./habits.json")

        if self.dialog_habbit_number == "":
            showinfo("Error", "Choose a habit fom dashboard")
            return

        item_id = self.dialog_habbit_number
        item_id = int(item_id) - 1

        selected_habit = Habit(
            loaded_data[item_id]["title"],
            loaded_data[item_id]["description"],
            loaded_data[item_id]["frequency"],
            loaded_data[item_id]["category"],
            loaded_data[item_id]["significance"],
            loaded_data[item_id]["progress_entries"],
            loaded_data[item_id]["last_done"],
            "edit",
            loaded_data[item_id]["habit_id"]
        )
        selected_habit.successes = loaded_data[item_id]["successes"]
        selected_habit.current_streak = loaded_data[item_id]["current_streak"]
        selected_habit.longest_streak = loaded_data[item_id]["longest_streak"]
        selected_habit.next_deadline = loaded_data[item_id]["next_deadline"]

        last_done = (datetime.fromisoformat(selected_habit.progress_entries[-1]["timestamp"])
                     if selected_habit.progress_entries and "timestamp" in selected_habit.progress_entries[-1]
                     else datetime(1969, 7, 20)) 
        if selected_habit.is_completed_today():
            showinfo("The habit is done", "The habit has been already done today!")
        elif (selected_habit.frequency == "weekly" 
              and last_done.isocalendar()[1] == datetime.now().isocalendar()[1] 
              and last_done.year == datetime.now().year):
            showinfo("The habit is done", "The habit has been already done this week!")
        elif (selected_habit.frequency == "monthly" 
              and last_done.month == datetime.now().month
              and last_done.year == datetime.now().year):
            showinfo("The habit is done", "The habit has been already done this month!")
        else:
            selected_habit.complete_habit()
            selected_habit.update_success_status()
            selected_habit.update_longest_streak()
            selected_habit.update_next_deadline()

            loaded_data[item_id]["last_done"] = selected_habit.last_done
            loaded_data[item_id]["successes"] = selected_habit.successes
            loaded_data[item_id]["current_streak"] = selected_habit.current_streak
            loaded_data[item_id]["longest_streak"] = selected_habit.longest_streak
            loaded_data[item_id]["next_deadline"] = selected_habit.next_deadline
            loaded_data[item_id]["progress_entries"] = selected_habit.progress_entries

            self.save_data(loaded_data, "habits.json")
            self.dialog_habbit_number = ""
            self.dash_func()
              
    def parse_date_time(self, date):
        """
        Parse a date string into a datetime object.

        Args:
            date (str): The date string to be parsed.

        Returns:
            datetime.datetime: A datetime object representing the parsed date.
        """
        return datetime.strptime(date, "%Y-%m-%d")
    
    def is_completed_today_app(self, selected_val):
        """
        Check if a habit was completed today based on the selected value.

        This function compares the date of the latest progress entry with 
        the current date to determine if the habit was completed today.

        Args:
            selectedVal (dict): The selected habit's data.

        Returns:
            bool: True if the habit was completed today, False otherwise.
        """
        if (selected_val["progress_entries"]
            and datetime.now().date() == datetime.fromisoformat(selected_val["progress_entries"][-1]["timestamp"]).date()):
            return True
        else: return False

    def metrics_func(self):
        """
        Display metrics information for a selected habit.

        This method displays metrics information about the selected habit, 
        including its name, creation date, last done date, streaks, progress, and more.
        """
        self.clear_frame()
        self.right_left_side_panel = customtkinter.CTkFrame(self.right_dashboard, 
                                                            width=100, 
                                                            corner_radius=10)
        self.right_left_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, 
                                        expand=False, padx=5, pady=5)
        self.selected_value_list = self.load_data("./habits.json")

        if len(self.selected_value_list) == 0:
            showinfo("No Habits In Your Database", 
                     "Enter a valid habit no or choose it from dashboard")
            self.dash_func()
            self.dialog_habbit_number = ""
        else: pass
        
        if self.dialog_habbit_number == "":
            showinfo("Enter a valid habit no", 
                     "Enter a valid habit no or choose it from dashboard")
            self.dash_func()
            self.dialog_habbit_number = ""
            return

        self.selected_value = self.selected_value_list[int(self.dialog_habbit_number)-1]
        self.dialog_habbit_number = ""
        
        self.logo_label_metric = customtkinter.CTkLabel(self.right_left_side_panel, 
                                                        text="Metrics  \n", 
                                                        font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label_metric.grid(row=1, column=0, padx=20, pady=(20, 10))
    
        self.bt_back = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Back", 
                                               command=self.dash_func)
        self.bt_back.grid(row=2, column=0, padx=20, pady=(100, 0))
        self.bt_back = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Open history", 
                                               command=partial(self.open_history, self.selected_value))
        self.bt_back.grid(row=2, column=0, padx=20, pady=(10, 0))

        self.right_right_side_panel = customtkinter.CTkFrame(self.right_dashboard, 
                                                             width=580, 
                                                             corner_radius=10)
        self.right_right_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, 
                                         expand=False, padx=5, pady=5)
        
        habit_labels = []
        habit_texts = ["Habit name: {}".format(self.selected_value["title"]), 
                       "Created on: {}".format(self.selected_value["start_date"]), 
                       "Last done on: {}".format(self.selected_value["last_done"]), 
                       "Current streak: {}".format(self.selected_value["current_streak"]), 
                       "Goal progress: {}/{}".format(self.selected_value["successes"], self.selected_value["goal"]), 
                       "Longest streak: {}".format(self.selected_value["longest_streak"])]
        for text_ in habit_texts:
            label = customtkinter.CTkLabel(master=self.right_right_side_panel, 
                                           width=580, 
                                           height=50, 
                                           corner_radius=10, 
                                           text_color="black",
                                           fg_color="grey", 
                                           text=text_, 
                                           anchor="w")
            label.grid(padx=0, pady=10)
            habit_labels.append(label)
        self.selected_value = []
    
    def analytics_func(self):
        """
        Display analytics information based on habit data.

        This method displays various analytics about habits, 
        including average remaining time, active habits, average streak length,
        habits within a certain period, top streaks, 
        highest success and failure rates, overall success and failure rates,
        top interval and category performance, and average streak breaks.
        """
        self.clear_frame()
        data = self.load_data("./habits.json")
        if data == []:
            showinfo("Error", "No habits availbale to show analytics.First add Habits")
            return
        
        def clear_frame():
            try:
                for wid in self.right_side_dash.winfo_children:
                    wid.destroy()
            except Exception as e:
                pass

        def make_table(format, data, result):
            clear_frame()
            try:
               self.right_side_dash.pack_forget()
            except Exception as e:
                pass

            if format == "remainingTime":
                self.right_side_dash = customtkinter.CTkFrame(self.right_dashboard)
                self.right_side_dash.pack(side=tkinter.LEFT, fill=tkinter.BOTH, 
                                          expand=True, pady=5 ,padx=(0, 5))
                cols = ["Habit", "Remaining Time"]
                treescroll = ttk.Scrollbar(self.right_side_dash,)
                treescroll.pack(side = "right", fill = "y")
                treeview = ttk.Treeview(self.right_side_dash, 
                                        show="headings", 
                                        yscrollcommand=treescroll.set, 
                                        columns=cols, height=13)
                treeview.pack(side="top", fill="both", expand=True, padx=5, pady=5)
                treescroll.config(command=treeview.yview)

                treeview.column("Habit", width=100)
                treeview.column("Remaining Time", width=200)

                treeview.heading("Habit", text="Habit")
                treeview.heading("Remaining Time", text="Remaining Time")

                count = 1
                for record in data:
                    remaining_time = (record["next_deadline"] - datetime.now()).days
                    lists = [record["title"], remaining_time]
                    treeview.insert(parent="", index=tkinter.END, iid=count, text="", values=lists)
                    count+=1

                lists = ["average", result]
                treeview.insert(parent="", index=tkinter.END, iid=count, text="", values=lists)

            if format == "activeHabits":
                self.right_side_dash = customtkinter.CTkFrame(self.right_dashboard)
                self.right_side_dash.pack(side=tkinter.LEFT, fill=tkinter.BOTH, 
                                          expand=True, pady=5 ,padx=(0, 5))
                cols = [
                    "Habit", 
                    "Last done", 
                    "Current streak", 
                    "Progress", 
                    "Done"
                ]
                treescroll = ttk.Scrollbar(self.right_side_dash,)
                treescroll.pack(side = "right", fill = "y")
                treeview = ttk.Treeview(self.right_side_dash,show="headings",
                                        yscrollcommand=treescroll.set, columns=cols, height=13)
                treeview.pack(side="top", fill="both", expand=True, padx=5, pady=5)
                treescroll.config(command=treeview.yview)
                
                treeview.column("Habit", width=140)
                treeview.column("Last done", width=125)
                treeview.column("Current streak", width=125)
                treeview.column("Progress", width=125)
                
                treeview.heading("Habit", text="Habit")
                treeview.heading("Last done", text="Last done")
                treeview.heading("Current streak", text="Current streak")
                treeview.heading("Progress", text="Progress")

                count = 1
                for record in data:
                    lists = [
                        record["title"],  
                        datetime.fromisoformat(record["progress_entries"][-1]["timestamp"]).date() if record["progress_entries"] else "-", 
                        record["current_streak"], 
                        "{}/{}".format(record["successes"], record["goal"])
                    ]
                    treeview.insert(parent="", index=tkinter.END, 
                                    iid=count, text="", values=lists)
                    count += 1

            if format == "streaklength": 
                self.right_side_dash = customtkinter.CTkFrame(self.right_dashboard)
                self.right_side_dash.pack(side=tkinter.LEFT, fill=tkinter.BOTH, 
                                          expand=True, pady=5, padx=(0, 5))
                cols = ["Habit", "Streak Length"]
                treescroll = ttk.Scrollbar(self.right_side_dash,)
                treescroll.pack(side = "right", fill = "y")
                treeview = ttk.Treeview(self.right_side_dash, show="headings", 
                                        yscrollcommand=treescroll.set, columns=cols, height=13)
                treeview.pack(side="top", fill="both", expand=True, padx=5, pady=5)
                treescroll.config(command=treeview.yview)

                treeview.column("Habit", width=100)
                treeview.column("Streak Length", width=200)

                treeview.heading("Habit", text="Habit")
                treeview.heading("Streak Length", text="Streak Length")

                count = 1
                for record in data:
                    lists = [record["title"], record["longest_streak"]]
                    treeview.insert(parent="", index=tkinter.END, iid=count, 
                                    text="", values=lists)
                    count += 1

                lists = ["average", result]
                treeview.insert(parent="", index=tkinter.END, 
                                iid=count, text="", values=lists)

            if format == "topStreak":
                self.right_side_dash = customtkinter.CTkFrame(self.right_dashboard)
                self.right_side_dash.pack(side=tkinter.LEFT, fill=tkinter.BOTH, 
                                          expand=True, pady=5, padx=(0, 5))
                cols = ["Habit", "Longest streak"]
                treescroll = ttk.Scrollbar(self.right_side_dash)
                treescroll.pack(side="right", fill="y")
                treeview = ttk.Treeview(self.right_side_dash, 
                                        show="headings", 
                                        yscrollcommand=treescroll.set, 
                                        columns=cols, 
                                        height=13)
                treeview.pack(side="top", fill="both", expand=True, padx=5, pady=5)
                treescroll.config(command=treeview.yview)

                treeview.column("Habit", width=100)
                treeview.column("Longest streak", width=200)

                treeview.heading("Habit", text="Habit")
                treeview.heading("Longest streak", text="Longest streak")

                count = 1
                for record, streak in zip(data, result):
                    lists = [record["title"], streak]
                    treeview.insert(parent="", index=tkinter.END, iid=count, 
                                    text="", values=lists)
                    count += 1

        def make_habits_with_frequency_table():
            def submit():
                habits_with_frequency = analytics_methods.habits_with_frequency(habits, frequency.get())
                make_table("activeHabits", 
                           [habit.__dict__  for habit in habits_with_frequency], 
                           habits_with_frequency)

            clear_frame()
            try:
               self.right_side_dash.pack_forget()
            except Exception as e:
                pass

            self.right_side_dash = customtkinter.CTkFrame(self.right_dashboard)
            self.right_side_dash.pack(side=tkinter.LEFT, fill=tkinter.BOTH, 
                                      expand=True, pady=5, padx=(0, 5))

            text_label = customtkinter.CTkLabel(self.right_side_dash, 
                                                text="Choose frequency to display", 
                                                font=customtkinter.CTkFont(size=20))
            text_label.pack(pady=(25, 5))
            frequency = customtkinter.CTkOptionMenu(master=self.right_side_dash,
                                                    values=["daily", "weekly", "monthly"],
                                                    command=lambda choice: choice)
            frequency.set("daily")
            frequency.pack(pady=5)
            get_date_btn = customtkinter.CTkButton(self.right_side_dash, 
                                                    text="Show habits", 
                                                    command=submit)
            get_date_btn.pack(pady=10)

        def make_habits_in_period_table(mode, text=""):
            def get_date_and_submit():
                st = start_date.get_date()
                et = end_date.get_date()

                habits_in_period = analytics_methods.habits_in_period(data, st, et)
                make_table("activeHabits", [d.__dict__  for d in habits_in_period], 
                           habits_in_period)

            clear_frame()
            try:
               self.right_side_dash.pack_forget()
            except Exception as e:
                pass

            self.right_side_dash = customtkinter.CTkFrame(self.right_dashboard)
            self.right_side_dash.pack(side=tkinter.LEFT, fill=tkinter.BOTH, 
                                      expand=True, pady=5, padx=(0, 5))

            if mode == "single":
                text_label = customtkinter.CTkLabel(self.right_side_dash, 
                                                   text=text, 
                                                   font=customtkinter.CTkFont(size=20))
                text_label.pack(pady=100)
            elif mode == "table":
                text_label = customtkinter.CTkLabel(self.right_side_dash, 
                                                   text="Enter Start Date", 
                                                   font=customtkinter.CTkFont(size=20))
                text_label.pack(pady=5)
                start_date = DateEntry(self.right_side_dash, background="#242424")
                start_date.pack(pady=10)
                text_label = customtkinter.CTkLabel(self.right_side_dash, 
                                                   text="Enter End Date", 
                                                   font=customtkinter.CTkFont(size=20))
                text_label.pack(pady=5)
                end_date = DateEntry(self.right_side_dash, background="#242424")
                end_date.pack(pady=10)
                get_date_btn = customtkinter.CTkButton(self.right_side_dash, 
                                                     text="Get Active Habits", 
                                                     command=get_date_and_submit)
                get_date_btn.pack(pady=10)

        habits = []
        for datum in data:
            current = Habit(
                        datum["title"], 
                        datum["description"], 
                        datum["frequency"], 
                        datum["category"], 
                        datum["significance"], 
                        datum["progress_entries"], 
                        datum["last_done"], 
                        "edit",
                        datum["habit_id"]
            )
            current.start_date = datetime.fromisoformat(datum["start_date"]).date()
            current.successes = datum["successes"]
            current.current_streak = datum["current_streak"]
            current.longest_streak = datum["longest_streak"]
            current.next_deadline = datum["next_deadline"]
            current.goal = datum["goal"]
            habits.append(current)
        analytics_methods = Analytics()

        self.right_left_side_panel = customtkinter.CTkFrame(self.right_dashboard, 
                                                            width=100, 
                                                            corner_radius=10)
        self.right_left_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, 
                                        expand=False, padx=5, pady=5)
    
        self.right_left_side_panel.grid_columnconfigure(0, weight=1)
        self.right_left_side_panel.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8,
                                                      9, 10, 11, 12, 13, 14, 15), 
                                                      weight=0)
        
        self.goal_label = customtkinter.CTkLabel(self.right_left_side_panel, 
                                                      text="Choose an option", 
                                                      font=customtkinter.CTkFont(size=20, weight="bold"))
        self.goal_label.grid(row=1, column=0, padx=10, pady=(10, 5))
        
        analytics_button_width = 200
        def get_habit_and_value(habits, habit_id, prompt):
            for habit in habits:
                if habit.habit_id == habit_id:
                    return habit, prompt(habit)

        active_habits = analytics_methods.active_habits(habits)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Active habits", 
                                               width=analytics_button_width, 
                                               command=partial(make_table, 
                                                               "activeHabits", 
                                                               [habit.__dict__  for habit in active_habits], 
                                                               active_habits))
        self.bt_save.grid(row=2, column=0, padx=20, pady=(25, 0))

        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Habits of given frequency", 
                                               width=analytics_button_width, 
                                               command=make_habits_with_frequency_table)
        self.bt_save.grid(row=3, column=0, padx=20, pady=(5, 0))

        top_streak_habit_id = analytics_methods.top_streak_habit(habits)
        top_streak_habit, top_streak = get_habit_and_value(habits, 
                                                           top_streak_habit_id, 
                                                           lambda habit: habit.longest_streak)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Top streak habit", 
                                               width=analytics_button_width, 
                                               command=partial(make_habits_in_period_table, 
                                                               "single", 
                                                               f"The habit with best streak is {top_streak_habit.title}\n with a streak of {top_streak}"))
        self.bt_save.grid(row=4, column=0, padx=20, pady=(5, 0))

        longest_streaks = [analytics_methods.get_longest_streak(habit) for habit in habits]
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Longest streaks", 
                                               width=analytics_button_width, 
                                               command=partial(make_table, 
                                                               "topStreak", 
                                                               [habit.__dict__ for habit in habits], 
                                                               longest_streaks))
        self.bt_save.grid(row=5, column=0, padx=20, pady=(5, 0))

        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Habits in period", 
                                               width=analytics_button_width, 
                                               command=partial(make_habits_in_period_table, "table"))
        self.bt_save.grid(row=6, column=0, padx=20, pady=(5, 0))

        def success_rate(habit):
            days_since_creation = (datetime.now().date() - habit.start_date).days + 1
            if habit.frequency == "weekly":
                days_since_creation = datetime.now().date().isocalendar()[1] - habit.start_date.isocalendar()[1] + 1
            elif habit.frequency == "monthly":
                days_since_creation = ((datetime.now().date().year - habit.start_date.year) * 12 
                                        + (datetime.now().date().month - habit.start_date.month) - 1 - len(habit.progress_entries)) + 1
            days_with_progress = len(habit.progress_entries)
            return days_with_progress / days_since_creation if days_since_creation else 0
        highest_success_rate_id = analytics_methods.highest_success_rate(habits)
        highest_success_rate_habit, highest_success_rate = get_habit_and_value(habits, 
                                                                               highest_success_rate_id, 
                                                                               success_rate)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Highest success rate", 
                                               width=analytics_button_width, 
                                               command=partial(make_habits_in_period_table, 
                                                               "single", 
                                                               f"The habit with highest success rate is {highest_success_rate_habit.title}\n with a success rate of {highest_success_rate:.2f}"))
        self.bt_save.grid(row=7, column=0, padx=20, pady=(5, 0))

        def failure_rate(habit):
            days_since_creation = (datetime.now().date() - habit.start_date).days + 1
            if habit.frequency == "weekly":
                days_since_creation = datetime.now().date().isocalendar()[1] - habit.start_date.isocalendar()[1] + 1
            elif habit.frequency == "monthly":
                days_since_creation = ((datetime.now().date().year - habit.start_date.year) * 12 
                                        + (datetime.now().date().month - habit.start_date.month) - len(habit.progress_entries)) + 1
            days_with_progress = len(habit.progress_entries)
            return (days_since_creation - days_with_progress) / days_since_creation if days_since_creation else 0
        highest_failure_rate_id = analytics_methods.highest_failure_rate(habits)
        highest_failure_rate_habit, highest_failure_rate = get_habit_and_value(habits,
                                                                               highest_failure_rate_id,
                                                                               failure_rate)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Highest failure rate", 
                                               width=analytics_button_width, 
                                               command=partial(make_habits_in_period_table, 
                                                               "single", 
                                                               f"The habit with highest failure rate is {highest_failure_rate_habit.title}\n with a failure rate of {highest_failure_rate:.2f}"))
        self.bt_save.grid(row=8, column=0, padx=20, pady=(5, 0))

        overall_success = analytics_methods.overall_successes(habits)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Total successes", 
                                               width=analytics_button_width, 
                                               command=partial(make_habits_in_period_table, 
                                                               "single", 
                                                               f"Your total number of successes is {overall_success}"))
        self.bt_save.grid(row=9, column=0, padx=20, pady=(5, 0))

        overall_failure = analytics_methods.overall_failures(habits)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Total failures", 
                                               width=analytics_button_width, 
                                               command=partial(make_habits_in_period_table, 
                                                               "single", 
                                                               f"Your total number of failures is {overall_failure}"))
        self.bt_save.grid(row=10, column=0, padx=20, pady=(5, 0))

        top_category_performance = analytics_methods.top_category_performance(habits)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Top category performance", 
                                               width=analytics_button_width, 
                                               command=partial(make_habits_in_period_table, 
                                                               "single", 
                                                               f"The category with best perfomance is {top_category_performance}"))
        self.bt_save.grid(row=11, column=0, padx=20, pady=(5, 0))

        top_frequency_performance = analytics_methods.top_frequency_performance(habits)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Top frequency performance",
                                               width=analytics_button_width, 
                                               command=partial(make_habits_in_period_table, 
                                                               "single", 
                                                               f"The frequency with best perfomance is {top_frequency_performance}"))
        self.bt_save.grid(row=12, column=0, padx=20, pady=(5, 0))

        average_streak_length = analytics_methods.average_streak_length(habits)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Average streak length", 
                                               width=analytics_button_width, 
                                               command=partial(make_habits_in_period_table, 
                                                               "single",
                                                               f"Your average streak length is {average_streak_length:.1f}"))
        self.bt_save.grid(row=13, column=0, padx=20, pady=(5, 0))

        average_streak_break = analytics_methods.average_streak_break(habits)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Average streak break", 
                                               width=analytics_button_width, 
                                               command=partial(make_habits_in_period_table, 
                                                               "single", 
                                                               f"Your average streak break is {average_streak_break:.1f}"))
        self.bt_save.grid(row=14, column=0, padx=20, pady=(5, 0))

        average_remaining_time = analytics_methods.average_remaining_time(habits)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Average remaining time", 
                                               width=analytics_button_width, 
                                               command=partial(make_habits_in_period_table, 
                                                               "single",
                                                               f"Your average remaining time is {average_remaining_time:.1f} day(s)"))
        self.bt_save.grid(row=15, column=0, padx=20, pady=(5, 0))

    def edit_func(self):
        """
        Display an edit page for a selected habit.
        
        This method loads a list of habits, lets the user select a habit to edit,
        and then displays an edit page where the user can modify habit information.
        """
        self.selected_value_list = self.load_data("./habits.json")

        if len(self.selected_value_list) == 0:
            showinfo("No Habits In Your Database", 
                     "Enter a valid habit no or choose it from dashboard")
            self.dash_func()
            self.dialog_habbit_number = ""
        else: pass
        
        if self.dialog_habbit_number == "":
            showinfo("Enter a valid habit no", 
                     "Enter a valid habit no or choose it from dashboard")
            self.dash_func()
            self.dialog_habbit_number = ""
            return

        self.selected_value = self.selected_value_list[int(self.dialog_habbit_number) - 1]
        self.clear_frame()

        self.right_left_side_panel = customtkinter.CTkFrame(self.right_dashboard, 
                                                            width=100, 
                                                            corner_radius=10)
        self.right_left_side_panel.pack(side=tkinter.LEFT, 
                                        fill=tkinter.Y, 
                                        expand=False, 
                                        padx=5, 
                                        pady=5)
        self.right_left_side_panel.grid_columnconfigure(0, weight=1)
        self.right_left_side_panel.grid_rowconfigure((0, 1, 2, 3), weight=0)
        self.right_left_side_panel.grid_rowconfigure((4, 5), weight=1)
        
        self.goal_label = customtkinter.CTkLabel(self.right_left_side_panel, 
                                                      text="Edit Page! \n", 
                                                      font=customtkinter.CTkFont(size=20, weight="bold"))
        self.goal_label.grid(row=1, column=0, padx=20, pady=(20, 10))
    
        
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Save changes", 
                                               command=partial(self.save_changes, 
                                                               "edit", 
                                                               self.dialog_habbit_number, 
                                                               self.selected_value["progress_entries"]))
        self.bt_save.grid(row=2, column=0, padx=20, pady=(100, 0))
        
        def optionmenu_callback(choice):
            pass

        self.combobox = customtkinter.CTkOptionMenu(master=self.right_left_side_panel,
                                                    values=["daily", "weekly", "monthly"],
                                                    command=optionmenu_callback)
        self.combobox.grid(row=3, column=0, padx=20, pady=(10,0))
        self.combobox.set(self.selected_value["frequency"])

        self.bt_delete = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                                 text="Delete", 
                                                 command=partial(self.delete_func, 
                                                                 self.dialog_habbit_number))
        self.bt_delete.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.bt_cancel = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                                 text="Cancel", 
                                                 command=self.dash_func)
        self.bt_cancel.grid(row=4, column=0, padx=20, pady=(200, 0))

        self.right_right_side_panel = customtkinter.CTkFrame(self.right_dashboard, 
                                                             width=580, 
                                                             corner_radius=10)
        self.right_right_side_panel.pack(side=tkinter.LEFT, 
                                         fill=tkinter.BOTH, 
                                         expand=True, 
                                         padx=5, 
                                         pady=5)
        
        self.right_right_bottom_side_panel = customtkinter.CTkFrame(self.right_right_side_panel,
                                                                    width=580, 
                                                                    corner_radius=10)
        self.right_right_bottom_side_panel.pack(side="top", fill="both")
        
        self.habit_name_label_edit = customtkinter.CTkLabel(self.right_right_bottom_side_panel,
                                                            text="Habit name", 
                                                            font=customtkinter.CTkFont(size=20, weight="bold"))
        self.habit_name_label_edit.pack(pady=(25, 0))

        self.habit_name_entry = customtkinter.CTkEntry(master=self.right_right_bottom_side_panel, 
                                                       corner_radius=10, 
                                                       fg_color="black", 
                                                       width=550, 
                                                       height=50)
        self.habit_name_entry.insert(0, self.selected_value["title"])
        self.habit_name_entry.pack(padx=0, pady=20)
        
        self.habit_description_label_edit = customtkinter.CTkLabel(self.right_right_bottom_side_panel, 
                                                                   text="Habit description", 
                                                                   font=customtkinter.CTkFont(size=20, weight="bold"))
        self.habit_description_label_edit.pack()

        self.habit_description_entry = customtkinter.CTkEntry(master=self.right_right_bottom_side_panel, 
                                                              corner_radius=10, 
                                                              fg_color="black", 
                                                              width=550, 
                                                              height=50)
        self.habit_description_entry.insert(0, self.selected_value["description"])
        self.habit_description_entry.pack(padx=0, pady=20)

        self.category_label_edit = customtkinter.CTkLabel(self.right_right_side_panel, 
                                                text="Category", 
                                                font=customtkinter.CTkFont(size=20, weight="bold"))
        self.category_label_edit.pack()

        self.category_entry = customtkinter.CTkEntry(master=self.right_right_side_panel, 
                                                     corner_radius=10, 
                                                     fg_color="black", 
                                                     width=550, 
                                                     height=50)
        self.category_entry.insert(0, self.selected_value["category"])
        self.category_entry.pack(padx=0, pady=20)
        
        self.goal_label_edit = customtkinter.CTkLabel(self.right_right_bottom_side_panel, 
                                                      text="Goal", 
                                                      font=customtkinter.CTkFont(size=20, weight="bold"))
        self.goal_label_edit.pack()

        self.goal_entry = customtkinter.CTkEntry(master=self.right_right_bottom_side_panel, 
                                                 corner_radius=10, 
                                                 fg_color="black", 
                                                 width=550, 
                                                 height=50)
        self.goal_entry.insert(0, self.selected_value["goal"])
        self.goal_entry.pack(padx=0, pady=20)
    
    def open_history(self, selected):
        """
        Open a history window to display when the habit was marked.

        This method creates a new top-level window to show the history of when
        the habit was marked as completed. The history is displayed in a treeview.

        Args:
        selected (dict): The selected habit's data.
        """
        top_level = customtkinter.CTkToplevel(self)
        top_level.geometry("600x400")
        top_level.resizable(False, False)
        top_level.title("Last times when you mark the habits")
        progress_list = selected["progress_entries"]
        top_level.wm_attributes('-topmost', 1)

        cols = ["Date", "Time"]
        treescroll = ttk.Scrollbar(top_level,)
        treescroll.pack(side="right", fill="y")
        treeview = ttk.Treeview(top_level, 
                                show="headings", 
                                yscrollcommand=treescroll.set, 
                                columns=cols, 
                                height=13)
        treeview.pack(side="top",
                      fill="both", 
                      expand=True, 
                      padx=5, 
                      pady=5)
        treescroll.config(command=treeview.yview)
        
        treeview.column("Date", width=200)
        treeview.column("Time", width=200)
        
        treeview.heading("Date", text="Date")
        treeview.heading("Time", text="Time")

        count = 1
        for record in progress_list:
            timestamp = datetime.fromisoformat(record["timestamp"])
            lists = [timestamp.date(), timestamp.time()]
            treeview.insert(parent="", 
                            index=tkinter.END, 
                            iid=count, 
                            text="", 
                            values=lists)
            count += 1
    
    def change_scaling_event(self, new_scaling: str):
        """
        Change the scaling factor for widgets based on user input.

        This method changes the scaling factor for the widgets in the application
        based on the provided scaling percentage.

        Args:
        new_scaling (str): The new scaling percentage as a string (e.g., "125%").
        """
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
 
    def close_window(self):
        """
        Close the application window.

        This method closes the application window.
        """ 
        App.destroy(self)
          
    def clear_frame(self):
        """
        Clear the contents of the right dashboard frame.

        This method removes all widgets from the right dashboard frame.
        """
        for widget in self.right_dashboard.winfo_children():
            widget.destroy()

a = App()
a.mainloop()