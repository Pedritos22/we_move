import tkinter as tk
from sds import JournalApp
from self_goals import TaskApp  # Ensure TaskApp is properly defined in self_goals

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("HackYeah2024")
        self.master.geometry("400x300")
        self.master.configure(bg='#F7E3D3')

        label = tk.Label(self.master, text="bawi", font=("Helvetica", 28), bg='#F7E3D3')
        label.pack(pady=20)

        # Create two buttons to launch the applications
        journal_button = tk.Button(self.master, text="Yournal", command=self.open_journal_app,
                                   bg='#FF8C69', fg='white', font=("Helvetica", 14, "bold"),
                                   relief='flat', bd=0, padx=20, pady=10)
        journal_button.pack(pady=10, ipadx=30, ipady=10)

        task_button = tk.Button(self.master, text="Self Goals", command=self.open_task_app,
                                 bg='#FF8C69', fg='white', font=("Helvetica", 14, "bold"),
                                 relief='flat', bd=0, padx=20, pady=10)
        task_button.pack(pady=10, ipadx=30, ipady=10)

    def open_journal_app(self):
        try:
            # Open Journal App in a new window
            new_window = tk.Toplevel(self.master)
            journal_app = JournalApp(new_window)
        except Exception as e:
            print(f"Error opening journal app: {e}")

    def open_task_app(self):
        try:
            # Open Task App in a new window
            new_window = tk.Toplevel(self.master)
            task_app = TaskApp(new_window)  # Pass the new_window parameter
        except Exception as e:
            print(f"Error opening task app: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
