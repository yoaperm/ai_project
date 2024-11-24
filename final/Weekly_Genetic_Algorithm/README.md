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
