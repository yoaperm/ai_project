# Genetic Algorithm Scheduling Project

This repository contains scripts, documentation, and notebooks for implementing and comparing Genetic Algorithms (GA) and Compact Genetic Algorithms (cGA) to optimize scheduling problems.

## Table of Contents
- [Project Overview](#project-overview)
- [Final Folder Structure](#final-folder-structure)
- [Daily Genetic Algorithm](#daily-genetic-algorithm)
- [Weekly Genetic Algorithm](#weekly-genetic-algorithm)
- [Time Space Comparison](#time-space-comparison)
- [Video Presenting](#video-presenting)
- [Presentation](#presentation)

## Project Overview
This project aims to explore different GA techniques, including traditional GA and compact GA, for optimizing scheduling problems, specifically a weekly timetable for a master's degree student. The goal is to compare their performance in terms of time consumption, space usage, and fitness improvement.

## Final Folder Structure
The repository is structured into three main components, each focusing on a distinct aspect of scheduling optimization. This separation ensures clarity in understanding the different use cases and methodologies applied.

### Final/
- **Time_Space_Comparison/**
  - `readme.md`: Documentation explaining the purpose of time and space comparisons.
  - `requirement.text`: Dependencies required to run the scripts in this folder.
  - Python file(s): Scripts to execute time and space comparison experiments.

- **Daily_Genetic_Algorithm/**
  - `readme.md`: Documentation describing the daily optimization script.
  - `requirement.text`: Dependencies for running the daily scheduling script.
  - Python file(s): Script for daily schedule optimization using GA.

- **Weekly_Genetic_Algorithm/**
  - `readme.md`: Documentation detailing the weekly optimization script.
  - `requirement.text`: Dependencies for running the weekly scheduling script.
  - Python file(s): Script for weekly schedule optimization using GA.

## Daily Genetic Algorithm

The `Daily_Genetic_Algorithm` folder contains all scripts and documentation for optimizing daily schedules using Genetic Algorithms (GA), balancing productivity and tension across various activities. The goal is to create a schedule that maximizes productivity while maintaining a healthy work-life balance, where each hour of the day must be optimized for various activities such as work, rest, and study. This level of granularity requires a specific approach that differs from broader weekly planning.

## Weekly Genetic Algorithm

The `Weekly_Genetic_Algorithm` folder contains scripts for optimizing a weekly schedule using Genetic Algorithms (GA). The weekly schedule aims to balance work, study, rest, and other activities over the span of a week, considering the unique constraints that occur during weekends and specific weekdays. The optimization must account for specific days when tasks like office work or studying harder subjects should be planned, taking into account fatigue and other constraints.


## Time Space Comparison

The purpose of the `Time_Space_Comparison` folder is to compare the execution time and memory usage between different scheduling optimization techniques.

### Time Comparison: GA vs Brute Force
- This comparison focuses on evaluating the execution time required to solve the scheduling problem using Genetic Algorithm (GA) versus a brute-force approach.
- As the number of bits (i.e., complexity) increases, the brute-force method becomes significantly slower due to the exponential growth in possible solutions, whereas GA maintains better efficiency by intelligently searching the solution space.
- The results demonstrate that GA is more efficient in terms of execution time, especially as the problem complexity grows, making it a preferable approach for larger scheduling problems.

### Space Comparison: GA vs Compact Genetic Algorithm (cGA)
- The comparison also includes memory usage between GA and Compact Genetic Algorithm (cGA).
- cGA is designed to use less memory by representing the population probabilistically rather than maintaining an explicit population of individuals, making it suitable for environments with limited memory resources.
- The comparison results show that cGA significantly reduces memory usage compared to the traditional GA while achieving comparable results in terms of optimization quality.

## Video Presenting

The `AI Project - Time Scheduling by Genetic Algorithm.mp4` file contains video presentations that demonstrate the implementation and results of the scheduling optimization techniques discussed in this project.
- The videos explain how the Genetic Algorithm (GA), Brute Force, and Compact Genetic Algorithm (cGA) approaches are used to solve scheduling problems.
- Visual demonstrations of the weekly scheduling optimization process, including charts and comparisons, are provided to illustrate the improvements achieved by GA over traditional methods.

## Presentation

The `Time Scheduling.pptx` file contains the slides used to present the project overview, methodology, and results.
- The slides cover key aspects such as the problem definition, Genetic Algorithm concepts, implementation details, and performance comparisons.
- Visual aids and charts are included to help convey the efficiency and effectiveness of GA and cGA in solving scheduling problems.

