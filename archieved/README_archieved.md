# Genetic Algorithm Scheduling Project

This repository contains scripts, documentation, and notebooks for implementing and comparing Genetic Algorithms (GA) and Compact Genetic Algorithms (cGA) to optimize scheduling problems.

## Table of Contents
- [Project Overview](#project-overview)
- [Weekly Scheduling](#weekly-scheduling)
- [Daily Scheduling](#daily-scheduling)
- [Time and Space Comparison](#time-and-space-comparison)
- [Video Presenting](#video-presenting)
- [Presentation](#presentation)

## Project Overview
This project aims to explore different GA techniques, including traditional GA and compact GA, for optimizing scheduling problems, specifically a weekly timetable for a master's degree student. The goal is to compare their performance in terms of time consumption, space usage, and fitness improvement.

## Weekly Scheduling

The `weekly_genetic_algorithm.py` script in this project is designed to create an optimized weekly schedule for a master's degree student using a Genetic Algorithm (GA). The script schedules activities such as work, classes, sleep, exercise, and other daily routines to balance productivity, well-being, and personal time over a typical week.

### Key Features:
- **Chromosome Structure**: Each chromosome represents a complete weekly schedule, consisting of genes for each hour of each day (7 days x 24 hours).
- **Mandatory Activities**: The script schedules mandatory activities such as work, university classes, and sleep based on predefined requirements and constraints. For example, specific days are designated as work-from-home or office days, and sleep is scheduled during preferred hours.
- **Fitness Function**: The fitness function evaluates how well a chromosome meets predefined requirements, such as achieving a certain number of work hours, sleep hours, and including beneficial activities like exercise. Penalties are applied for failing to meet these requirements, ensuring the schedule meets the student's needs.
- **Genetic Operators**:
  - **Selection**: Tournament selection is used to choose the best chromosomes for the next generation.
  - **Crossover**: Parent chromosomes are combined to produce offspring, creating diversity in the population.
  - **Mutation**: Random mutations are applied to introduce variations in the schedule while respecting the time constraints for mandatory activities.
- **Visualization**: The script generates visualizations of the schedules using stacked bar charts, allowing a comparison between the initial best schedule and the optimized schedule after running the GA.

### Workflow:
1. **Initialization**: A population of random chromosomes is generated, each representing a potential weekly schedule.
2. **Fitness Evaluation**: Each chromosome is evaluated using a fitness function, with scores reflecting how well it balances various tasks and personal needs.
3. **GA Loop**: Over multiple generations, chromosomes are selected, crossed over, and mutated to find the optimal schedule.
4. **Visualization**: The script creates visual comparisons between the initial and optimized schedules, demonstrating the improvements made by the GA.

### Visualization Examples:
The script produces stacked bar charts that show how the student's time is allocated each day for different activities. These visualizations help understand the improvements in activity allocation after running the GA.

### Usage:
- The script can be executed to generate a weekly schedule that aims to optimize the balance between work, study, rest, and leisure.
- The resulting schedules provide insights into time management strategies for a busy master's student, helping to achieve an optimal work-life balance while ensuring productivity and well-being.

## Daily Scheduling

The `daily_genetic_algorithm.py` script is designed to optimize daily schedules using Genetic Algorithms (GA), balancing productivity and tension across various activities. The goal is to create a schedule that maximizes productivity while maintaining a healthy work-life balance.

### Key Variables Explained:
- **HOURS_IN_DAY**: `24` – Represents the total hours in a day.
- **MIN_SLEEP_HOURS**: `7` – Minimum required hours of sleep.
- **MAX_WORK_STUDY_HOURS**: `12` – Maximum combined work and study hours.

### Activities:
- A comprehensive set of daily activities, including Work, Study, Rest/Nap, Sleep, Exercise, Meals, Leisure, Socializing, Personal Care, and Commuting.

### Genetic Algorithm Settings:
- **NGEN**: Number of generations (`150`).
- **MU**: Size of the parent population (`300`).
- **LAMBDA**: Number of offspring generated per generation (`400`).
- **CXPB**: Crossover probability (`0.7`).
- **MUTPB**: Mutation probability (`0.2`).

### Enhanced Logic and Constraints:
- **Minimum Work and Study Hours**: Ensures a realistic balance for working professionals and students.
- **Balanced Life**: Rewards for keeping work, study, and sleep within 70% of daily hours.
- **Leisure and Socializing Minimum**: Ensures healthy work-life balance.
- **Exercise Requirement**: Encourages physical activity for overall well-being.
- **Meals and Personal Care**: Ensures basic necessities are not neglected.

### Visualizations:
- **Bar Charts**: Compare initial and optimized schedules, showing activity reallocation.
- **Gantt Charts**: Illustrate time blocks for each activity in the initial and optimized schedules.
- **Pareto Front Plots**: Show the trade-off between productivity and tension, highlighting optimal solutions.

### Insights:
- The daily schedule optimization provides a flexible framework to adapt to individual preferences, balancing productivity with well-being and realistic constraints.

## Time and Space Comparison

The purpose of the `time_space_comparison` folder is to compare the execution time and memory usage between different scheduling optimization techniques.

### Time Comparison: GA vs Brute Force
- This comparison focuses on evaluating the execution time required to solve the scheduling problem using Genetic Algorithm (GA) versus a brute-force approach.
- As the number of bits (i.e., complexity) increases, the brute-force method becomes significantly slower due to the exponential growth in possible solutions, whereas GA maintains better efficiency by intelligently searching the solution space.
- The results demonstrate that GA is more efficient in terms of execution time, especially as the problem complexity grows, making it a preferable approach for larger scheduling problems.

### Space Comparison: GA vs Compact Genetic Algorithm (cGA)
- The comparison also includes memory usage between GA and Compact Genetic Algorithm (cGA).
- cGA is designed to use less memory by representing the population probabilistically rather than maintaining an explicit population of individuals, making it suitable for environments with limited memory resources.
- The comparison results show that cGA significantly reduces memory usage compared to the traditional GA while achieving comparable results in terms of optimization quality.

### Folder Contents
- All scripts, datasets, and results related to time and space comparisons are available in the `time_space_comparison` folder.

## Video Presenting

This section contains video presentations that demonstrate the implementation and results of the scheduling optimization techniques discussed in this project.
- The videos explain how the Genetic Algorithm (GA), Brute Force, and Compact Genetic Algorithm (cGA) approaches are used to solve scheduling problems.
- Visual demonstrations of the weekly scheduling optimization process, including charts and comparisons, are provided to illustrate the improvements achieved by GA over traditional methods.

## Presentation

The `presentation` folder contains the slides used to present the project overview, methodology, and results.
- The slides cover key aspects such as the problem definition, Genetic Algorithm concepts, implementation details, and performance comparisons.
- Visual aids and charts are included to help convey the efficiency and effectiveness of GA and cGA in solving scheduling problems.

