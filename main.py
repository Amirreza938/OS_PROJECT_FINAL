import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from time import sleep
from sub_systems.main_system import MainSystem
from sub_systems.sub_system_1.sub_system_1 import SubSystem1
from task import SubSystem1Task
from task import SubSystem2Task
from task import SubSystem3Task
from sub_systems.sub_system_3.sub_system_3 import SubSystem3
from sub_systems.sub_system_2.sub_system_2 import SubSystem2
from resource_manager import ResourceManager
import logging
import threading

logging.getLogger().setLevel(logging.CRITICAL)  # Suppress all logs below CRITICAL level

class InputDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Input Parameters")
        self.parent = parent
        self.result = None

        # Resource inputs
        self.total_r1_label = tk.Label(self, text="Total R1:")
        self.total_r1_label.grid(row=0, column=0, padx=5, pady=5)
        self.total_r1_entry = tk.Entry(self)
        self.total_r1_entry.grid(row=0, column=1, padx=5, pady=5)

        self.total_r2_label = tk.Label(self, text="Total R2:")
        self.total_r2_label.grid(row=1, column=0, padx=5, pady=5)
        self.total_r2_entry = tk.Entry(self)
        self.total_r2_entry.grid(row=1, column=1, padx=5, pady=5)

        # Subsystem 1 inputs
        self.sub1_tasks_label = tk.Label(self, text="Number of Tasks for SubSystem1:")
        self.sub1_tasks_label.grid(row=2, column=0, padx=5, pady=5)
        self.sub1_tasks_entry = tk.Entry(self)
        self.sub1_tasks_entry.grid(row=2, column=1, padx=5, pady=5)

        # Subsystem 2 inputs
        self.sub2_tasks_label = tk.Label(self, text="Number of Tasks for SubSystem2:")
        self.sub2_tasks_label.grid(row=3, column=0, padx=5, pady=5)
        self.sub2_tasks_entry = tk.Entry(self)
        self.sub2_tasks_entry.grid(row=3, column=1, padx=5, pady=5)

        # Subsystem 3 inputs
        self.sub3_tasks_label = tk.Label(self, text="Number of Tasks for SubSystem3:")
        self.sub3_tasks_label.grid(row=4, column=0, padx=5, pady=5)
        self.sub3_tasks_entry = tk.Entry(self)
        self.sub3_tasks_entry.grid(row=4, column=1, padx=5, pady=5)

        self.submit_button = tk.Button(self, text="Submit", command=self.on_submit)
        self.submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    def on_submit(self):
        try:
            total_r1 = int(self.total_r1_entry.get())
            total_r2 = int(self.total_r2_entry.get())
            sub1_tasks = int(self.sub1_tasks_entry.get())
            sub2_tasks = int(self.sub2_tasks_entry.get())
            sub3_tasks = int(self.sub3_tasks_entry.get())

            # Collect task details for SubSystem1
            sub1_task_details = []
            for i in range(sub1_tasks):
                task_details = simpledialog.askstring(
                    "Input Task Details",
                    f"Enter SubSystem1 Task {i+1} details (name,exec_time,r1_need,r2_need,arrival_time,core):"
                )
                if task_details:
                    sub1_task_details.append(task_details.split(","))

            # Collect task details for SubSystem2
            sub2_task_details = []
            for i in range(sub2_tasks):
                task_details = simpledialog.askstring(
                    "Input Task Details",
                    f"Enter SubSystem2 Task {i+1} details (name,exec_time,r1_need,r2_need,arrival_time,core):"
                )
                if task_details:
                    sub2_task_details.append(task_details.split(","))

            # Collect task details for SubSystem3
            sub3_task_details = []
            for i in range(sub3_tasks):
                task_details = simpledialog.askstring(
                    "Input Task Details",
                    f"Enter SubSystem3 Task {i+1} details (name,exec_time,r1_need,r2_need,arrival_time,period):"
                )
                if task_details:
                    sub3_task_details.append(task_details.split(","))

            self.result = (total_r1, total_r2, sub1_task_details, sub2_task_details, sub3_task_details)
            self.destroy()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers for resources and number of tasks.")

class SimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Simulation")
        
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
        self.text_area.pack(padx=10, pady=10)
        
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)
        
        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_simulation)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop_simulation, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.resume_button = tk.Button(self.button_frame, text="Resume", command=self.resume_simulation, state=tk.DISABLED)
        self.resume_button.pack(side=tk.LEFT, padx=5)
        
        self.simulation_thread = None
        self.simulation_running = False
        self.simulation_paused = False
        self.simulation_lock = threading.Lock()  # Lock for thread safety

    def print_system_state(self, main_system, current_time):
        self.text_area.insert(tk.END, f"Time: {current_time}\n\n")
        
        for i, sub_system in enumerate(main_system.sub_systems):
            if isinstance(sub_system, SubSystem1):
                self.text_area.insert(tk.END, "Sub1:\n")
                self.text_area.insert(tk.END, f"Resources: R1: {sub_system.r1_assigned} R2: {sub_system.r2_assigned}\n")
                
                waiting_queue_tasks = [task.name for task in list(sub_system.waiting_queue)]
                self.text_area.insert(tk.END, f"Waiting Queue: {waiting_queue_tasks}\n")
                
                for j, core in enumerate(sub_system.cores):
                    self.text_area.insert(tk.END, f"Core{j+1}:\n")
                    task = core.get_current_task()
                    if task:
                        self.text_area.insert(tk.END, f"Running Task: {task.name}\n")
                    else:
                        self.text_area.insert(tk.END, "Running Task: idle\n")
                    
                    ready_queue_tasks = [task.name for task in list(core.ready_queue)]
                    self.text_area.insert(tk.END, f"Ready Queue: {ready_queue_tasks}\n")
                self.text_area.insert(tk.END, "\n")
            
            elif isinstance(sub_system, SubSystem2):
                self.text_area.insert(tk.END, "Sub2:\n")
                self.text_area.insert(tk.END, f"Resources: R1: {sub_system.r1_assigned} R2: {sub_system.r2_assigned}\n")
                self.text_area.insert(tk.END, f"Ready Queue: {[task.name for task in list(sub_system.scheduler.ready_queue)]}\n")
                
                for j, core in enumerate(sub_system.cores):
                    self.text_area.insert(tk.END, f"Core{j+1}:\n")
                    task = core.get_current_task()
                    if task:
                        self.text_area.insert(tk.END, f"Running Task: {task.name}\n")
                    else:
                        self.text_area.insert(tk.END, "Running Task: idle\n")
                self.text_area.insert(tk.END, "\n")
            
            elif isinstance(sub_system, SubSystem3):
                self.text_area.insert(tk.END, "Sub3:\n")
                self.text_area.insert(tk.END, f"Resources: R1: {sub_system.r1_assigned} R2: {sub_system.r2_assigned}\n")
                self.text_area.insert(tk.END, f"Waiting Queue: {[task.name for task in list(sub_system.scheduler.ready_queue)]}\n")
                self.text_area.insert(tk.END, f"Ready Queue: {[task.name for task in list(sub_system.scheduler.ready_queue)]}\n")
                
                self.text_area.insert(tk.END, "Core1:\n")
                task = sub_system.core.get_current_task()
                if task:
                    self.text_area.insert(tk.END, f"Running Task: {task.name}\n")
                else:
                    self.text_area.insert(tk.END, "Running Task: idle\n")
                self.text_area.insert(tk.END, "\n")
        
        self.text_area.insert(tk.END, "hello\n")  # Print "hello" only once per iteration
        self.text_area.see(tk.END)

    def start_simulation(self):
        # Open the input dialog to get user inputs
        input_dialog = InputDialog(self.root)
        self.root.wait_window(input_dialog)

        if input_dialog.result is None:
            return  # User closed the dialog without submitting

        total_r1, total_r2, sub1_task_details, sub2_task_details, sub3_task_details = input_dialog.result

        with self.simulation_lock:
            self.simulation_running = True
            self.simulation_paused = False
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)
        
        self.simulation_thread = threading.Thread(target=self.run_simulation, args=(total_r1, total_r2, sub1_task_details, sub2_task_details, sub3_task_details))
        self.simulation_thread.start()

    def stop_simulation(self):
        with self.simulation_lock:
            self.simulation_paused = True
            self.stop_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.NORMAL)

    def resume_simulation(self):
        with self.simulation_lock:
            self.simulation_paused = False
            self.stop_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)

    def run_simulation(self, total_r1, total_r2, sub1_task_details, sub2_task_details, sub3_task_details):
        # Initialize ResourceManager
        resource_manager = ResourceManager(total_r1, total_r2)

        # Create tasks for SubSystem1
        sub1_tasks = []
        for task_details in sub1_task_details:
            name, exec_time, r1_need, r2_need, arrival_time, core = task_details
            task = SubSystem1Task(name, int(exec_time), int(r1_need), int(r2_need), int(arrival_time), int(core))
            sub1_tasks.append(task)

        # Create tasks for SubSystem2
        sub2_tasks = []
        for task_details in sub2_task_details:
            name, exec_time, r1_need, r2_need, arrival_time, core = task_details
            task = SubSystem2Task(name, int(exec_time), int(r1_need), int(r2_need), int(arrival_time), int(core))
            sub2_tasks.append(task)

        # Create tasks for SubSystem3
        sub3_tasks = []
        for task_details in sub3_task_details:
            name, exec_time, r1_need, r2_need, arrival_time, period = task_details
            task = SubSystem3Task(name, int(exec_time), int(r1_need), int(r2_need), int(arrival_time), int(period))
            sub3_tasks.append(task)

        resource_1_finish_flag = False
        resource_2_finish_flag = False
        resource_3_finish_flag = False

        # Initialize subsystems
        sub_system_1 = SubSystem1(total_r1, total_r2, [1, 1, 1], 4, 4, sub1_tasks, resource_1_finish_flag, 1)
        sub_system_2 = SubSystem2(resource_manager, 4, 4, sub2_tasks, resource_2_finish_flag, 2)
        sub_system_3 = SubSystem3(resource_manager, 4, 4, sub3_tasks, resource_3_finish_flag, 3)

        # Create main system with all subsystems
        main_system = MainSystem([sub_system_1, sub_system_2, sub_system_3], total_r1, total_r2)
        main_system.start()
        
        current_time = 0
        while self.simulation_running:
            with self.simulation_lock:
                if self.simulation_paused:
                    sleep(0.1)
                    continue

            main_system.toggle_clock()
            self.print_system_state(main_system, current_time)
            current_time += 1
            sleep(1)

            # Check if all tasks are completed
            if all([sub_system.finish_flag for sub_system in main_system.sub_systems]):
                break
        
        with self.simulation_lock:
            self.simulation_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.DISABLED)

if __name__ == '__main__':
    root = tk.Tk()
    app = SimulationApp(root)
    root.mainloop()