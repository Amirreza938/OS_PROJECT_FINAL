from time import sleep

from sub_systems.main_system import MainSystem
from sub_systems.sub_system_1.sub_system_1 import SubSystem1
from task import SubSystem1Task
from task import SubSystem2Task
from sub_systems.sub_system_2.sub_system_2 import SubSystem2

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
    queue_weights = [1, 1]

    #task: SubSystem1Task = SubSystem1Task("T1", 10, 1, 1,3, 0)
    task: SubSystem2Task = SubSystem2Task("T1",10,1,1,0,2)
    task1: SubSystem2Task = SubSystem2Task("T2",10,1,1,1,2)
    task2: SubSystem2Task = SubSystem2Task("T3",10,1,1,2,2)
    resource_1_finish_flag = False
    resource_2_finish_flag = False
    #sub_system_1 = SubSystem1(total_resources, queue_weights, 4, 4, [task], resource_1_finish_flag)
    sub_system_2 = SubSystem2(total_resources,4,4,[task,task1,task2],resource_2_finish_flag)
    main_system = MainSystem([sub_system_2])
    main_system.start()

    for _ in range(100):
        main_system.toggle_clock()
        print("hello")
        sleep(1)


if __name__ == '__main__':
    main()