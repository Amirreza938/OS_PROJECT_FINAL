import tkinter as tk
from tkinter import scrolledtext
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
        with self.simulation_lock:
            self.simulation_running = True
            self.simulation_paused = False
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)
        
        self.simulation_thread = threading.Thread(target=self.run_simulation)
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

    def run_simulation(self):
        total_r1 = 10
        total_r2 = 10

        # Initialize ResourceManager
        resource_manager = ResourceManager(total_r1, total_r2)

        # Tasks for SubSystem1
        task1: SubSystem1Task = SubSystem1Task("T1", 10, 1, 1, 0, 1)
        task2: SubSystem1Task = SubSystem1Task("T2", 10, 1, 1, 1, 2)
        task3: SubSystem1Task = SubSystem1Task("T3", 10, 1, 1, 2, 3)

        # Tasks for SubSystem2
        task4: SubSystem2Task = SubSystem2Task("T4", 10, 1, 1, 0, 1)
        task5: SubSystem2Task = SubSystem2Task("T5", 10, 1, 1, 1, 2)

        # Task for SubSystem3
        task6: SubSystem3Task = SubSystem3Task("T6", 10, 1, 1, 0, 20)

        resource_1_finish_flag = False
        resource_2_finish_flag = False
        resource_3_finish_flag = False

        # Initialize subsystems
        sub_system_1 = SubSystem1(total_r1, total_r2, [1, 1, 1], 4, 4, [task1, task2, task3], resource_1_finish_flag, 1)
        sub_system_2 = SubSystem2(resource_manager, 4, 4, [task4, task5], resource_2_finish_flag, 2)
        sub_system_3 = SubSystem3(resource_manager, 4, 4, [task6], resource_3_finish_flag, 3)

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