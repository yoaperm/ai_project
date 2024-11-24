# Genetic Algorithm Scheduling Project

This repository contains scripts, documentation, and notebooks for implementing and comparing Genetic Algorithms (GA) and Compact Genetic Algorithms (cGA) to optimize scheduling problems.

## Table of Contents
- [Project Overview](#project-overview)
- [Weekly Scheduling](#weekly-scheduling)
- [Daily Scheduling](#daily-scheduling)
- [Time and Space Comparison](#time-space-comparison])

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


## Time And Space Comparison

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

