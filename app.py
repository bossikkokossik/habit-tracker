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
import habit

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
                                                    command=self.mark_done_func, 
                                                    state="disabled")
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
            "Frequency", 
            "Last Done", 
            "Current Streak", 
            "Progress", 
            "Done"
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
        treeview.column("Description", width=200)
        treeview.column("Frequency", width=100)
        treeview.column("Last Done", width=100)
        treeview.column("Current Streak", width=100)
        treeview.column("Progress", width=100)
        
        treeview.heading("Habit", text="Habit")
        treeview.heading("Description", text="Description")
        treeview.heading("Frequency", text="Frequency")
        treeview.heading("Last Done", text="Last Done")
        treeview.heading("Current Streak", text="Current Streak")
        treeview.heading("Progress", text="Progress")
        self.loaded_data = self.load_data("habits.json")
        self.lists += self.loaded_data
        count = 1
        for record in self.loaded_data:
            lists = [
                record["title"], 
                record["description"], 
                record["frequency"], 
                record["progress_entries"][-1]["date"], 
                record["current_streak"], 
                "{}/{}".format(record["successes"],record["days"])
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
                selectedVal = self.loaded_data[int(item_id)-1]
                if selectedVal["progress_entries"][-1]["date"] == datetime.now().strftime("%Y-%m-%d"):
                    self.bt_mark_done.configure(state="disabled")
                else:
                    self.bt_mark_done.configure(state="normal")
                self.bt_add_habit.configure(state="normal")
                self.bt_metrics.configure(state="normal")
            except Exception as e:
                pass
            if item_id and button_id == "#6":
                self.dialog_habbit_number = item_id
                self.edit_func()
            elif item_id and button_id == "#7":
                self.delete_func(item_id)
            elif item_id and button_id == "#8":
                self.dialog_habbit_number = item_id
                self.metrics_func()

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
            json.dump(data, file)

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
        category = "habits"
        significance = self.goal_entry.get()
        habit_id = self.id + 1
        self.id = habit_id    
        frequency = self.combobox.get()
        title = self.habit_name_entry.get()
        description = self.habit_description_entry.get()
        progress_entries = [{"date": "none", "time": "none"}]
        end_date = ["Have not been marked down"]
        
        habits = habit.Habit(habit_id,title, description, frequency, category, 
                             significance, progress_entries, end_date, "add")
        habits.update_next_deadline()
        if frequency == "daily":
            habits.days = int(significance)
        elif frequency == "weekly":
            habits.days = int(significance) * 7
        elif frequency == "monthly":
            habits.days = int(significance) * 30
        data.append({
            "habit_id": habits.habit_id, 
            "title": habits.title,
            "description": habits.description,
            "active": habits.active,
            "start_date": habits.start_date,
            "end_date": habits.end_date,
            "frequency": habits.frequency,
            "successes": habits.successes,
            "current_streak": habits.current_streak,
            "longest_streak": habits.longest_streak,
            "category": habits.category,
            "notify": habits.notify,
            "significance": habits.significance,
            "next_deadline": habits.next_deadline,
            "progress_entries": habits.progress_entries,
            "days": habits.days
        })
        self.save_data(data,"habits.json")
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
        category = "habits"
        significance = self.goal_entry.get()
        habit_id = id
        self.id = habit_id    
        self.dialog_habbit_number = ""
        frequency = self.combobox.get()
        title = self.habit_name_entry.get()
        description = self.habit_description_entry.get()
        progress_entries = progess_entries
        end_date = ["Have not been marked down"]

        habits = habit.Habit(habit_id,title, description, frequency, category,
                             significance, progress_entries,end_date, mode, id)
        habits.update_next_deadline()
        
        if frequency == "daily":
            habits.days = int(significance)
        elif frequency == "weekly":
            habits.days = int(significance)*7
        elif frequency == "monthly":
            habits.days = int(significance)*30

        self.selected_value_list[int(self.id)-1]["habit_id"] = habit_id
        self.selected_value_list[int(self.id)-1]["title"] = title
        self.selected_value_list[int(self.id)-1]["description"] = description
        self.selected_value_list[int(self.id)-1]["frequency"] = frequency
        self.selected_value_list[int(self.id)-1]["category"] = category
        self.selected_value_list[int(self.id)-1]["significance"] = significance
        self.selected_value_list[int(self.id)-1]["progress_entries"] = progress_entries
        self.selected_value_list[int(self.id)-1]["end_date"] = end_date
                           
        self.save_data(self.selected_value_list, "habits.json")
        self.dash_func()

    def delete_func(self, itemId):
        """
        Delete a habit and update the data.

        This function deletes a habit based on the given itemId and updates the data accordingly.

        Args:
            itemId (str): The ID of the habit to be deleted.
        """
        self.dialog_habbit_number = ""
        data = self.load_data("./habits.json")
        for index, item in enumerate(data):
             if int(item["habit_id"]) > int(itemId)-1:
                 data[index]["habit_id"] = str(int(data[index]["habit_id"]) - 1)   
        del data[int(itemId) - 1]
        self.save_data(data, "./habits.json")
        self.dash_func()
           
    def save_changes(self, mode, id="", progess_entries=[{"date": "none", "time": "none"}]):
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
        
        self.logo_label_edit = customtkinter.CTkLabel(self.right_left_side_panel, 
                                                      text="Add Habit Page! \n", 
                                                      font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label_edit.grid(row=1, column=0, padx=20, pady=(20, 10))
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Save", command=self.adding_func)
        self.bt_save.grid(row=2, column=0, padx=20, pady=(100, 0))
        def optionmenu_callback(choice):
            return choice
        self.combobox = customtkinter.CTkOptionMenu(master=self.right_left_side_panel,
                                                    values=["daily", "weekly", "monthly"],
                                                    command=optionmenu_callback)
        self.combobox.grid(row=3, column=0, padx=20, pady=(10,0))
        self.combobox.set("Select Periodicity")
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
                                                       text="Habit Name \n", 
                                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        self.habit_name_label.pack()
        self.habit_name_entry = customtkinter.CTkEntry(master=self.right_right_side_panel, 
                                                       corner_radius=10, 
                                                       fg_color="black", 
                                                       width=555, 
                                                       height=50)
        self.habit_name_entry.pack(padx=0, pady=20)
        self.logo_label = customtkinter.CTkLabel(self.right_right_side_panel, 
                                                 text="Habit Description \n", 
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.pack()
        self.habit_description_entry = customtkinter.CTkEntry(master=self.right_right_side_panel, 
                                                              corner_radius=10, 
                                                              fg_color="black", 
                                                              width=555, height=50)
        self.habit_description_entry.pack(padx=0, pady=20)
        self.logo_label_edit = customtkinter.CTkLabel(self.right_right_side_panel, 
                                                text="Goal \n", 
                                                font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label_edit.pack()
        self.goal_entry = customtkinter.CTkEntry(master=self.right_right_side_panel, 
                                                 corner_radius=10, 
                                                 fg_color="black", 
                                                 width=555, 
                                                 height=50)
        self.goal_entry.pack(padx=0, pady=20)
        
    def mark_done_func(self):
        """
        Mark a habit as done for the current date.

        This function updates the progress and streak information for a habit when it is marked as done for the current date.
        """
        date = datetime.now().strftime("%Y-%m-%d")
        currentTime = datetime.now().strftime("%H:%M:%S")
        loadedData = self.load_data("./habits.json")

        if self.dialog_habbit_number == "":
            showinfo("Error", "Choose a habit fom dashboard")
            return

        itemId = self.dialog_habbit_number
        itemId = int(itemId) - 1

        if loadedData[itemId]["progress_entries"][-1]["date"] == date:
            showinfo("The Habit is Done", "THe Habit is done Today")

        if loadedData[itemId]["progress_entries"][-1]["date"] != date:
            loadedData[itemId]["successes"] = int(loadedData[itemId]["successes"]) + 1
            loadedData[itemId]["current_streak"] = int(loadedData[itemId]["current_streak"]) + 1
            loadedData[itemId]["progress_entries"].append({"date": date, "time": currentTime}) 
            if self.is_completed_today_app(loadedData[itemId]):
                loadedData[itemId]["longest_streak"] += 1
            else: loadedData[itemId]["longest_streak"] = 0
            if loadedData[itemId]["current_streak"] >= loadedData[itemId]["longest_streak"]:
                loadedData[itemId]["longest_streak"] = loadedData[itemId]["current_streak"]

            self.save_data(loadedData, "habits.json")
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
    
    def is_completed_today_app(self, selectedVal):
        """
        Check if a habit was completed today based on the selected value.

        This function compares the date of the latest progress entry with 
        the current date to determine if the habit was completed today.

        Args:
            selectedVal (dict): The selected habit's data.

        Returns:
            bool: True if the habit was completed today, False otherwise.
        """
        if datetime.now() == self.parse_date_time(selectedVal["progress_entries"][-1]["date"]):
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
                                               text="Open History", 
                                               command=partial(self.openHistory, self.selected_value))
        self.bt_back.grid(row=2, column=0, padx=20, pady=(10, 0))

        self.right_right_side_panel = customtkinter.CTkFrame(self.right_dashboard, 
                                                             width=580, 
                                                             corner_radius=10)
        self.right_right_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, 
                                         expand=False, padx=5, pady=5)
        
        habit_labels = []
        if self.selected_value["progress_entries"][-1]["date"] == "none":
            self.selected_value["end_date"] = "Never"
        else:
            self.selected_value["end_date"] = (
                self.selected_value["progress_entries"][-1]["date"] 
                + " at " + self.selected_value["progress_entries"][-1]["time"]
            )
        habit_texts = ["Habit name: {}".format(self.selected_value["title"]), 
                       "Created on: {}".format(self.selected_value["start_date"]), 
                       "First done on: {}".format(self.selected_value["start_date"]), 
                       "Last done on: {}".format(self.selected_value["end_date"]), 
                       "Current Streak: {}".format(self.selected_value["current_streak"]), 
                       "Goal Compliation progress: {}/{}".format(self.selected_value["successes"], self.selected_value["days"]), 
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
        
        def clearFrame():
            try:
                for wid in self.right_side_dash.winfo_children:
                    wid.destroy()
            except Exception as e:
                pass

        def makeTable(formate, data, result):
            clearFrame()
            try:
               self.right_side_dash.pack_forget()
            except Exception as e:
                pass

            if formate == "remainingTime":
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
                    remainingTime = (record["next_deadline"] - datetime.now()).days
                    lists = [record["title"], remainingTime]
                    treeview.insert(parent="", index=tkinter.END, iid=count, text="", values=lists)
                    count+=1

                lists = ["average", result]
                treeview.insert(parent="", index=tkinter.END, iid=count, text="", values=lists)

            if formate == "activeHabits":
                self.right_side_dash = customtkinter.CTkFrame(self.right_dashboard)
                self.right_side_dash.pack(side=tkinter.LEFT, fill=tkinter.BOTH, 
                                          expand=True, pady=5 ,padx=(0, 5))
                cols = [
                    "Active Habits", 
                    "Description", 
                    "Last Done", 
                    "Current Streak", 
                    "Progress", 
                    "Done"
                ]
                treescroll = ttk.Scrollbar(self.right_side_dash,)
                treescroll.pack(side = "right", fill = "y")
                treeview = ttk.Treeview(self.right_side_dash,show="headings",
                                        yscrollcommand=treescroll.set, columns=cols, height=13)
                treeview.pack(side="top", fill="both", expand=True, padx=5, pady=5)
                treescroll.config(command=treeview.yview)
                
                treeview.column("Active Habits", width=100)
                treeview.column("Description", width=200)
                treeview.column("Last Done", width=100)
                treeview.column("Current Streak", width=100)
                treeview.column("Progress", width=100)
                
                treeview.heading("Active Habits", text="Active Habits")
                treeview.heading("Description", text="Description")
                treeview.heading("Last Done", text="Last Done")
                treeview.heading("Current Streak", text="Current Streak")
                treeview.heading("Progress", text="Progress")

                count = 1
                for record in data:
                    lists = [
                        record["title"], 
                        record["description"], 
                        record["progress_entries"][-1]["date"], 
                        record["current_streak"], 
                        "{}/{}".format(record["successes"], record["days"])
                    ]
                    treeview.insert(parent="", index=tkinter.END, 
                                    iid=count, text="", values=lists)
                    count += 1

            if formate == "streaklength": 
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

            if formate == "topStreak":
                self.right_side_dash = customtkinter.CTkFrame(self.right_dashboard)
                self.right_side_dash.pack(side=tkinter.LEFT, fill=tkinter.BOTH, 
                                          expand=True, pady=5, padx=(0, 5))
                cols = ["Habit", "Top Streak"]
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
                treeview.column("Top Streak", width=200)

                treeview.heading("Habit", text="Habit")
                treeview.heading("Top Streak", text="Top Streak")

                count = 1
                for record in data:
                    lists = [record["title"], record["longest_streak"]]
                    treeview.insert(parent="", index=tkinter.END, iid=count, 
                                    text="", values=lists)
                    count += 1

                lists = ["Top Streak", result]
                treeview.insert(parent="", index=tkinter.END, iid=count, 
                                text="", values=lists)

        def habitInPeriadTableMaker(mode, text=""):
            def getDateandSubmit():
                st = startDate.get_date()
                et = endDate.get_date()

                st = datetime.combine(st, datetime.time(datetime.now()))
                et = datetime.combine(et, datetime.time(datetime.now()))

                habitsInPeriod = analytics_methods.habits_in_period(data, st, et)
                makeTable("activeHabits", [d.__dict__  for d in habitsInPeriod], 
                          habitsInPeriod)

            clearFrame()
            try:
               self.right_side_dash.pack_forget()
            except Exception as e:
                pass

            self.right_side_dash = customtkinter.CTkFrame(self.right_dashboard)
            self.right_side_dash.pack(side=tkinter.LEFT, fill=tkinter.BOTH, 
                                      expand=True, pady=5, padx=(0, 5))

            if mode == "single":
                textLabel = customtkinter.CTkLabel(self.right_side_dash, 
                                                   text=text, 
                                                   font=customtkinter.CTkFont(size=20))
                textLabel.pack(pady=100)
            elif mode == "table":
                textLabel = customtkinter.CTkLabel(self.right_side_dash, 
                                                   text="Enter Start Date", 
                                                   font=customtkinter.CTkFont(size=20))
                textLabel.pack(pady=5)
                startDate = DateEntry(self.right_side_dash, background="#242424")
                startDate.pack(pady=10)
                textLabel = customtkinter.CTkLabel(self.right_side_dash, 
                                                   text="Enter End Date", 
                                                   font=customtkinter.CTkFont(size=20))
                textLabel.pack(pady=5)
                endDate = DateEntry(self.right_side_dash, background="#242424")
                endDate.pack(pady=10)
                getDateBtn = customtkinter.CTkButton(self.right_side_dash, 
                                                     text="Get Active Habits", 
                                                     command=getDateandSubmit)
                getDateBtn.pack(pady=10)

        data = [Habit(d["habit_id"], 
                      d["title"], 
                      d["description"], 
                      d["frequency"], 
                      d["category"], 
                      d["significance"], 
                      d["progress_entries"], 
                      d["end_date"], 
                      "edit", 
                      "1", 
                      d["next_deadline"]) for d in data]
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
        
        self.logo_label_edit = customtkinter.CTkLabel(self.right_left_side_panel, 
                                                      text="Choose an option \n from Below", 
                                                      font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label_edit.grid(row=1, column=0, padx=10, pady=(20, 10))
    
        averageRemainingTime = analytics_methods.average_remaining_time(data)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Average Remaining Time", 
                                               command=partial(makeTable, 
                                                               "remainingTime", 
                                                               [d.__dict__  for d in data],
                                                               averageRemainingTime))
        self.bt_save.grid(row=2, column=0, padx=20, pady=(50, 0))
        
        activeHabits = analytics_methods.active_habits(data)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Active Habits", 
                                               width=155, 
                                               command=partial(makeTable, 
                                                               "activeHabits", 
                                                               [d.__dict__  for d in activeHabits], 
                                                               activeHabits))
        self.bt_save.grid(row=3, column=0, padx=20, pady=(5, 0))

        averageStreakLength = analytics_methods.average_streak_length(data)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Average Streak Length", 
                                               width=155, 
                                               command=partial(makeTable, 
                                                               "streaklength", 
                                                               [d.__dict__  for d in data], 
                                                               averageStreakLength))
        self.bt_save.grid(row=4, column=0, padx=20, pady=(5, 0))

        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Habits in Period", 
                                               width=155, 
                                               command=partial(habitInPeriadTableMaker, "table"))
        self.bt_save.grid(row=5, column=0, padx=20, pady=(5, 0))

        topStreakHabit = analytics_methods.top_streak_habit(data)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Top Streak", 
                                               width=155, 
                                               command=partial(makeTable, 
                                                               "topStreak", 
                                                               [d.__dict__  for d in data], 
                                                               topStreakHabit))
        self.bt_save.grid(row=6, column=0, padx=20, pady=(5, 0))

        highestSuccessRate = analytics_methods.highest_success_rate(data)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Highest Success Rate", 
                                               width=155, 
                                               command=partial(habitInPeriadTableMaker, 
                                                               "single", 
                                                               f"the heighest failure rate is {highestSuccessRate}"))
        self.bt_save.grid(row=7, column=0, padx=20, pady=(5, 0))

        highestFailureRate = analytics_methods.highest_failure_rate(data)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Highest Failure Rate", 
                                               width=155, 
                                               command=partial(habitInPeriadTableMaker, 
                                                               "single", 
                                                               f"the heighest failure rate is {highestFailureRate}"))
        self.bt_save.grid(row=8, column=0, padx=20, pady=(5, 0))

        overAllSuccess = analytics_methods.overall_successes(data)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Overall Success Rate", 
                                               width=155, 
                                               command=partial(habitInPeriadTableMaker, 
                                                               "single", 
                                                               f"Your Overall Success Rate is {overAllSuccess}"))
        self.bt_save.grid(row=9, column=0, padx=20, pady=(5, 0))

        overAllfailure = analytics_methods.overall_failures(data)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Overall Failure Rate", 
                                               width=155, 
                                               command=partial(habitInPeriadTableMaker, 
                                                               "single", 
                                                               f"Your Overall Failure Rate is {overAllfailure}"))
        self.bt_save.grid(row=10, column=0, padx=20, pady=(5, 0))

        topIntervalPerformance = analytics_methods.top_interval_performance(data)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Overall Failure Rate", 
                                               width=155, 
                                               command=partial(habitInPeriadTableMaker, 
                                                               "single", 
                                                               f"Your Top internal Perfomance is {topIntervalPerformance}"))
        self.bt_save.grid(row=11, column=0, padx=20, pady=(5, 0))

        topCatigoryPerformance = analytics_methods.top_category_performance(data)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Overall Failure Rate", 
                                               width=155, 
                                               command=partial(habitInPeriadTableMaker, 
                                                               "single", 
                                                               f"Your Top Catigory Perfomance is {topCatigoryPerformance}"))
        self.bt_save.grid(row=11, column=0, padx=20, pady=(5, 0))

        averageStreakBreak = analytics_methods.average_streak_break(data)
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Average Steak Beak", 
                                               width=155, 
                                               command=partial(habitInPeriadTableMaker, 
                                                               "single", 
                                                               f"Your average streak Break is {averageStreakBreak}"))
        self.bt_save.grid(row=11, column=0, padx=20, pady=(5, 0))

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
        
        self.logo_label_edit = customtkinter.CTkLabel(self.right_left_side_panel, 
                                                      text="Edit Page! \n", 
                                                      font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label_edit.grid(row=1, column=0, padx=20, pady=(20, 10))
    
        
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, 
                                               text="Save Changes", 
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
        self.combobox.set("Select Periodicity")

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
        
        self.right_right_top_side_panel = customtkinter.CTkFrame(self.right_right_side_panel,
                                                                 width=580, 
                                                                 corner_radius=10,
                                                                 fg_color="grey")
        self.right_right_top_side_panel.pack(side="top", fill="x")
        
        self.right_right_bottom_side_panel = customtkinter.CTkFrame(self.right_right_side_panel,
                                                                    width=580, 
                                                                    corner_radius=10)
        self.right_right_bottom_side_panel.pack(side="top", fill="both")
        
        self.habit_name_label_info = customtkinter.CTkLabel(self.right_right_top_side_panel, 
                                                            text="Habit Name: {} \n".format(self.selected_value["title"]), 
                                                            font=customtkinter.CTkFont(size=10, weight="bold"),
                                                            anchor="sw")
        self.habit_name_label_info.grid()

        self.habit_description_label = customtkinter.CTkLabel(self.right_right_top_side_panel, 
                                                              text="Habit Description: {} \n".format(self.selected_value["description"]), 
                                                              font=customtkinter.CTkFont(size=10, weight="bold"),
                                                              anchor="sw")
        self.habit_description_label.grid()

        self.goal_label = customtkinter.CTkLabel(self.right_right_top_side_panel, 
                                                 text="Goal: {} \n".format(self.selected_value["significance"]), 
                                                 font=customtkinter.CTkFont(size=10, weight="bold"),
                                                 anchor="sw")
        self.goal_label.grid()
        
        self.habit_name_label_edit = customtkinter.CTkLabel(self.right_right_bottom_side_panel,
                                                            text="Habit Name \n", 
                                                            font=customtkinter.CTkFont(size=20, weight="bold"))
        self.habit_name_label_edit.pack()

        self.habit_name_entry = customtkinter.CTkEntry(master=self.right_right_bottom_side_panel, 
                                                       corner_radius=10, 
                                                       fg_color="black", 
                                                       width=580, 
                                                       height=50)
        self.habit_name_entry.pack(padx=0, pady=20)
        
        self.habit_description_label_edit = customtkinter.CTkLabel(self.right_right_bottom_side_panel, 
                                                                   text="Habit Description \n", 
                                                                   font=customtkinter.CTkFont(size=20, weight="bold"))
        self.habit_description_label_edit.pack()

        self.habit_description_entry = customtkinter.CTkEntry(master=self.right_right_bottom_side_panel, 
                                                              corner_radius=10, 
                                                              fg_color="black", 
                                                              width=580, 
                                                              height=50)
        self.habit_description_entry.pack(padx=0, pady=20)
        
        self.goal_label_edit = customtkinter.CTkLabel(self.right_right_bottom_side_panel, 
                                                      text="Goal \n", 
                                                      font=customtkinter.CTkFont(size=20, weight="bold"))
        self.goal_label_edit.pack()

        self.goal_entry = customtkinter.CTkEntry(master=self.right_right_bottom_side_panel, 
                                                 corner_radius=10, 
                                                 fg_color="black", 
                                                 width=580, 
                                                 height=50)
        self.goal_entry.pack(padx=0, pady=20)
    
    def openHistory(self, selected):
        """
        Open a history window to display when the habit was marked.

        This method creates a new top-level window to show the history of when
        the habit was marked as completed. The history is displayed in a treeview.

        Args:
        selected (dict): The selected habit's data.
        """
        topLevel = customtkinter.CTkToplevel(self)
        topLevel.geometry("600x400")
        topLevel.resizable(False, False)
        topLevel.title("Last Times when you mark the habits")
        progessList = selected["progress_entries"]
        topLevel.wm_attributes('-topmost', 1)

        if len(progessList) > 1:
            del progessList[0]

        cols = ["Time", "Date"]
        treescroll = ttk.Scrollbar(topLevel,)
        treescroll.pack(side="right", fill="y")
        treeview = ttk.Treeview(topLevel,show="headings", 
                                yscrollcommand=treescroll.set, 
                                columns=cols, 
                                height=13)
        treeview.pack(side="top",
                      fill="both", 
                      expand=True, 
                      padx=5, 
                      pady=5)
        treescroll.config(command=treeview.yview)
        
        treeview.column("Time", width=200)
        treeview.column("Date", width=200)
        
        treeview.heading("Time", text="Time")
        treeview.heading("Date", text="Date")

        count = 1
        for record in progessList:
            lists = [record["date"], record["time"]]
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