# RT-Scheduling Operating System Project

## Table of Contents

1. [Introduction](#introduction)  
2. [Project Overview](#project-overview)  
3. [System Architecture](#system-architecture)  
4. [Subsystems](#subsystems)  
   - [SubSystem1](#subsystem1)  
   - [SubSystem2](#subsystem2)  
   - [SubSystem3](#subsystem3)  
5. [Task Scheduling Algorithms](#task-scheduling-algorithms)  
   - [Weighted Round Robin](#weighted-round-robin)  
   - [Shortest Remaining Time First](#shortest-remaining-time-first)  
   - [Rate Monotonic Scheduling](#rate-monotonic-scheduling)  
6. [Resource Management](#resource-management)  
7. [Implementation Steps](#implementation-steps)
8. [Project Structure](#project-structure)


---

## Introduction

This project is an implementation of a **real-time scheduling system** for an electric vehicle's electrical system. The system simulates how multiple subsystems manage tasks and resources efficiently while adhering to real-time constraints.

---

## Project Overview

The system is divided into three main subsystems:

1. **SubSystem1**: Implements the **Weighted Round Robin** scheduling algorithm.  
2. **SubSystem2**: Uses the **Shortest Remaining Time First (SRTF)** algorithm.  
3. **SubSystem3**: Employs **Rate Monotonic Scheduling (RMS)**, which is well-suited for real-time systems.  

Each subsystem operates independently and uses resources (`R1` and `R2`) managed by a centralized resource manager. Tasks are scheduled dynamically to ensure real-time execution without conflicts.

---

## System Architecture

The project is a **multi-threaded application** designed as follows:

- **MainSystem**: A central controller that initializes and manages subsystems.  
- **SubSystem1**: Uses a **Weighted Round Robin** scheduler with multiple cores.  
- **SubSystem2**: Implements **SRTF**, prioritizing tasks with the shortest remaining execution time.  
- **SubSystem3**: Uses **RMS**, prioritizing tasks based on their periodicity.  

---

## Subsystems

### SubSystem1

- **Cores**: 3 cores, each with its own ready queue.  
- **Scheduling Algorithm**: Weighted Round Robin.  
- **Resources**: Shares `R1` and `R2` dynamically.  
- **Queues**:  
  - **Ready Queue**: Tasks ready for execution.  
  - **Waiting Queue**: Tasks waiting for resources.  

---

### SubSystem2

- **Cores**: 2 cores with a shared ready queue.  
- **Scheduling Algorithm**: Shortest Remaining Time First (SRTF).  
- **Resources**: Allocates `R1` and `R2` dynamically.  
- **Queues**:  
  - **Ready Queue**: Tasks ready for execution.  
  - **No Waiting Queue**: Tasks are rejected if resources are unavailable.  

---

### SubSystem3

- **Cores**: 1 core with a single ready queue.  
- **Scheduling Algorithm**: Rate Monotonic Scheduling (RMS).  
- **Resources**: Allocates resources based on task deadlines.  
- **Queues**:  
  - **Ready Queue**: Tasks ready for execution.  
  - **Waiting Queue**: Tasks waiting for resources.  

---

## Task Scheduling Algorithms

### Weighted Round Robin

- **Description**: Tasks are distributed to cores based on weights. A core handles tasks in a round-robin manner, with weights determining task distribution.  
- **Application**: SubSystem1.

---

### Shortest Remaining Time First 

- **Description**: Prioritizes tasks with the shortest remaining execution time, ensuring shorter tasks are completed quickly.  
- **Application**: SubSystem2.

---

### Rate Monotonic Scheduling

- **Description**: Tasks are prioritized by their periods. Shorter-period tasks have higher priority.  
- **Application**: SubSystem3.

---

## Resource Management

A `ResourceManager` ensures proper allocation and release of shared resources (`R1` and `R2`):  

- **Allocation**: Dynamically assigned based on task requirements.  
- **Release**: Automatically freed when tasks complete or are re-queued.  

---


## Implementation Steps

The project was implemented in a structured and iterative manner, ensuring that each component was thoroughly tested before integrating it into the larger system. Below are the detailed steps we followed during the implementation:

---

### Step 1: Core, Task, and Resource Manager Classes

1. **Core Class**:
   - Implemented the `BaseCore` class, which serves as the foundation for all subsystem cores.
   - Added functionality for task execution, clock synchronization, and task scheduling.
   - Debugged the core logic to ensure tasks are executed correctly and resources are managed efficiently.

2. **Task Class**:
   - Created the `BaseTask` class, which defines the structure of tasks, including their states (`ready`, `running`, `waiting`, `finished`).
   - Extended the `BaseTask` class to create task-specific classes (`SubSystem1Task`, `SubSystem2Task`, `SubSystem3Task`) for each subsystem.
   - Added logging to track task execution and state changes.

3. **Resource Manager**:
   - Implemented the `ResourceManager` class to handle resource allocation and release.
   - Added methods to check resource availability (`can_allocate`) and allocate/release resources (`allocate`, `release`).
   - Tested resource management to ensure no deadlocks or resource conflicts occur.

---

### Step 2: Subsystems with Schedulers

1. **SubSystem1**:
   - Implemented `SubSystem1` with **Weighted Round Robin (WRR)** scheduling.
   - Created three cores, each with its own ready queue and a shared waiting queue.
   - Debugged the WRR scheduler to ensure tasks are distributed across cores based on their weights.
   - Tested resource allocation and task execution in isolation.

2. **SubSystem2**:
   - Implemented `SubSystem2` with **Shortest Remaining Time First (SRTF)** scheduling.
   - Created two cores with a single ready queue.
   - Debugged the SRTF scheduler to prioritize tasks with the shortest remaining execution time.
   - Tested dynamic task prioritization and resource management.

3. **SubSystem3**:
   - Implemented `SubSystem3` with **Rate Monotonic Scheduling (RMS)**.
   - Created a single core with a ready queue and a waiting queue.
   - Debugged the RMS scheduler to ensure tasks are executed based on their periods and deadlines.
   - Tested real-time task execution and resource allocation.

---

### Step 3: MainSystem Integration

1. **MainSystem**:
   - Implemented the `MainSystem` class to coordinate all subsystems.
   - Added functionality to toggle the clock for all subsystems simultaneously.
   - Integrated the subsystems (`SubSystem1`, `SubSystem2`, `SubSystem3`) into the `MainSystem`.
   - Debugged the integration to ensure subsystems work together without conflicts.

2. **Input and Output Testing**:
   - Created sample input tasks for each subsystem to test the system's behavior.
   - Verified the output at each time unit to ensure tasks are executed correctly and resources are allocated as expected.
   - Fixed any issues related to task scheduling, resource allocation, or subsystem coordination.

---

### Step 4: Final Testing and Debugging

1. **System-Wide Testing**:
   - Ran the entire system with multiple tasks across all subsystems.
   - Monitored the output to ensure tasks are executed in the correct order and resources are managed efficiently.
   - Checked for deadlocks, resource conflicts, or scheduling errors.

2. **Edge Cases**:
   - Tested edge cases such as:
     - Tasks with high resource requirements.
     - Tasks arriving at the same time.
     - Tasks with dependencies or deadlines.
   - Verified that the system handles these cases gracefully.

3. **Performance Optimization**:
   - Optimized the scheduling algorithms and resource management logic to improve system performance.
   - Reduced unnecessary logging and improved the efficiency of task execution.

---


## Project Structure

1. **Root Directory**:
   - `.gitignore`: Git ignore file.
   - `README.md`: Documentation for the project.
   - `main.py`: Main entry point of the program.
   - `resource_manager.py`: Manages resource allocation.
   - `task.py`: Task management and execution logic.
   - `requirements.txt`: Lists all dependencies required for the project.

2. **`sub_systems/` Directory**:
   - `main_system.py`: Orchestrates the interactions between subsystems.

   1. **SubSystem 1 (`sub_system_1/`)**:
      - `__init__.py`: Marks the directory as a Python package.
      - `sub_system_1.py`: Core logic for Subsystem 1.
      - `weighted_round_robin.py`: Implements the Weighted Round Robin scheduling algorithm.
      - `__pycache/`: Python bytecode cache.

   2. **SubSystem 2 (`sub_system_2/`)**:
      - `__init__.py`: Marks the directory as a Python package.
      - `sub_system_2.py`: Core logic for Subsystem 2.
      - `shortest_remaining_job_first.py`: Implements the Shortest Remaining Job First scheduling algorithm.
      - `__pycache/`: Python bytecode cache.

   3. **SubSystem 3 (`sub_system_3/`)**:
      - `__init__.py`: Marks the directory as a Python package.
      - `sub_system_3.py`: Core logic for Subsystem 3.
      - `rate_monotonic.py`: Implements the Rate Monotonic scheduling algorithm.
      - `__pycache/`: Python bytecode cache.


