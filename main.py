from time import sleep
from sub_systems.main_system import MainSystem
from sub_systems.sub_system_1.sub_system_1 import SubSystem1
from task import SubSystem1Task
from task import SubSystem2Task
from task import SubSystem3Task
from sub_systems.sub_system_3.sub_system_3 import SubSystem3
from sub_systems.sub_system_2.sub_system_2 import SubSystem2
import logging
logging.getLogger().setLevel(logging.CRITICAL)  # Suppress all logs below CRITICAL level
def print_system_state(main_system, current_time):
    print(f"Time: {current_time}\n")
    
    for i, sub_system in enumerate(main_system.sub_systems):
        if isinstance(sub_system, SubSystem1):
            print("Sub1:")
            print(f"Resources: R1: {sub_system.r1_assigned} R2: {sub_system.r2_assigned}")
            
            # Extract task names from the waiting queue
            waiting_queue_tasks = [task.name for task in list(sub_system.waiting_queue)]
            print(f"Waiting Queue: {waiting_queue_tasks}")
            
            for j, core in enumerate(sub_system.cores):
                print(f"Core{j+1}:")
                task = core.get_current_task()
                if task:
                    print(f"Running Task: {task.name}")
                else:
                    print("Running Task: idle")
                
                # Extract task names from the core's ready queue
                ready_queue_tasks = [task.name for task in list(core.ready_queue)]
                print(f"Ready Queue: {ready_queue_tasks}")
            print()
        
        elif isinstance(sub_system, SubSystem2):
            print("Sub2:")
            print(f"Resources: R1: {sub_system.r1_assigned} R2: {sub_system.r2_assigned}")
            print(f"Ready Queue: {[task.name for task in list(sub_system.scheduler.ready_queue)]}")
            
            for j, core in enumerate(sub_system.cores):
                print(f"Core{j+1}:")
                task = core.get_current_task()
                if task:
                    print(f"Running Task: {task.name}")
                else:
                    print("Running Task: idle")
            print()
        
        elif isinstance(sub_system, SubSystem3):
            print("Sub3:")
            print(f"Resources: R1: {sub_system.r1_assigned} R2: {sub_system.r2_assigned}")
            print(f"Waiting Queue: {[task.name for task in list(sub_system.scheduler.ready_queue)]}")
            print(f"Ready Queue: {[task.name for task in list(sub_system.scheduler.ready_queue)]}")
            
            print("Core1:")
            task = sub_system.core.get_current_task()
            if task:
                print(f"Running Task: {task.name}")
            else:
                print("Running Task: idle")
            print()


    


def main():
    total_resources = {
        'R1': 10,
        'R2': 10,
    }
    sub_system_1_resource_requester = {
        'R1': 4,
        'R2': 4
    }
    sub_system_2_resource_requester = {
        'R1': 4,
        'R2': 4
    }
    sub_system_3_resource_requester = {
        'R1' : 4,
        'R2' : 4
    }
    queue_weights = [1, 1]

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
    sub_system_1 = SubSystem1(total_resources, queue_weights, 4, 4, [task1, task2, task3], resource_1_finish_flag)
    sub_system_2 = SubSystem2(total_resources, 4, 4, [task4, task5], resource_2_finish_flag)
    sub_system_3 = SubSystem3(total_resources, 4, 4, [task6], resource_3_finish_flag)

    # Create main system with all subsystems
    main_system = MainSystem([sub_system_1, sub_system_2, sub_system_3])
    main_system.start()
    
    for current_time in range(100):
        main_system.toggle_clock()
        print_system_state(main_system, current_time)
        print("hello")  # Print "hello" only once per iteration
        sleep(1)

if __name__ == '__main__':
    main()