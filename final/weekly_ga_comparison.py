import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Parameters
DAYS = 7  # Number of days in the schedule
TIME_SLOTS = 24  # Hours in a day
WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# Activity dictionary with priority levels
activities = {
    'sleep': 1,
    'commute': 0,
    'work': 4,
    'study': 2,
    'homework': 3,
    'thesis': 5,
    'exercise': 2,
    'rest': 0
}

# Define time constraints
sleep_hours = list(range(22, 24)) + list(range(0, 6))  # Sleep from 22:00 to 06:00
work_hours = list(range(9, 18))  # Work from 09:00 to 18:00
commute_hours_morning = [8]  # Commute to work at 08:00 - 09:00
commute_hours_evening = [18]  # Commute from work at 18:00 - 19:00

# Define office days and remote days
office_days = ['Tue', 'Thu']
remote_days = ['Mon', 'Wed', 'Fri']

# Chromosome structure: DAYS * TIME_SLOTS genes
def create_chromosome():
    chromosome = []
    for day_index in range(DAYS):
        day = WEEKDAYS[day_index % 7]
        daily_schedule = []
        for hour in range(TIME_SLOTS):
            if hour in sleep_hours:
                daily_schedule.append('sleep')
            elif hour in commute_hours_morning and day in office_days:
                daily_schedule.append('commute')
            elif hour in commute_hours_evening and day in office_days:
                daily_schedule.append('commute')
            elif hour in work_hours:
                daily_schedule.append('work')
            else:
                # Available activities during free time
                possible_activities = ['study', 'homework', 'thesis', 'exercise', 'rest']
                activity = random.choice(possible_activities)
                daily_schedule.append(activity)
        chromosome.extend(daily_schedule)
    return chromosome

# Fitness function
def fitness(chromosome):
    score = 0
    for day_index in range(DAYS):
        day = WEEKDAYS[day_index % 7]
        daily_schedule = chromosome[day_index * TIME_SLOTS: (day_index + 1) * TIME_SLOTS]
        
        # Count activities
        sleep_hours_count = daily_schedule.count('sleep')
        work_hours_count = daily_schedule.count('work')
        thesis_hours = daily_schedule.count('thesis')
        exercise_hours = daily_schedule.count('exercise')
        study_hours = daily_schedule.count('study')
        
        # Sleep evaluation
        if sleep_hours_count >= 7:
            score += 10
        else:
            score -= 10  # Penalty for insufficient sleep
        
        # Work hours evaluation
        if work_hours_count != len(work_hours):
            score -= abs(work_hours_count - len(work_hours)) * 5  # Penalty for incorrect work hours
        
        # Avoid hard study on office days
        if day in office_days:
            hard_study_hours = daily_schedule.count('study')
            score -= 5 * hard_study_hours  # Penalty
        
        # Thesis work reward
        score += thesis_hours * 4
        
        # Exercise reward
        score += exercise_hours * 2
        
        # Penalty for activities during sleep hours
        for hour in sleep_hours:
            activity = daily_schedule[hour]
            if activity != 'sleep':
                score -= 5  # Penalty for not sleeping during sleep hours
        
        # Penalty for activities during work hours
        for hour in work_hours:
            activity = daily_schedule[hour]
            if activity not in ['work', 'commute']:
                score -= 5  # Penalty for non-work activities during work hours
        
        # Ensure total hours are 24
        if len(daily_schedule) != TIME_SLOTS:
            score -= 50  # Heavy penalty for incorrect day length
    
    return score

# Genetic Algorithm parameters
population_size = 100
generations = 500
mutation_rate = 0.5

# Initial population
population = [create_chromosome() for _ in range(population_size)]

# Evaluate fitness of initial population
fitness_scores = [fitness(chrom) for chrom in population]

# Find the best initial schedule
best_initial_fitness = max(fitness_scores)
best_initial_index = fitness_scores.index(best_initial_fitness)
best_initial_chromosome = population[best_initial_index]

print(f"Initial best fitness: {best_initial_fitness}")

# GA algorithm loop
for gen in range(generations):
    # Evaluate fitness
    fitness_scores = [fitness(chrom) for chrom in population]
    
    # Selection
    population = [chrom for _, chrom in sorted(zip(fitness_scores, population), reverse=True)]
    
    # Elitism
    next_generation = population[:int(0.2 * population_size)]  # Keep top 20%
    
    # Crossover
    while len(next_generation) < population_size:
        parent1 = random.choice(population[:int(0.5 * population_size)])
        parent2 = random.choice(population[:int(0.5 * population_size)])
        cross_point = random.randint(1, len(parent1) - 2)
        child1 = parent1[:cross_point] + parent2[cross_point:]
        child2 = parent2[:cross_point] + parent1[cross_point:]
        next_generation.extend([child1, child2])
    
    # Mutation
    for individual in next_generation[int(0.2 * population_size):]:  # Skip elites
        if random.random() < mutation_rate:
            mutate_point = random.randint(0, len(individual) - 1)
            day = mutate_point // TIME_SLOTS
            hour = mutate_point % TIME_SLOTS
            if hour in sleep_hours:
                new_activity = 'sleep'
            elif hour in commute_hours_morning + commute_hours_evening:
                new_activity = 'commute'
            elif hour in work_hours:
                new_activity = 'work'
            else:
                possible_activities = ['study', 'homework', 'thesis', 'exercise', 'rest']
                new_activity = random.choice(possible_activities)
            individual[mutate_point] = new_activity
    
    population = next_generation[:population_size]

# Evaluate final fitness scores
fitness_scores = [fitness(chrom) for chrom in population]

# Best schedule found after GA
best_fitness = max(fitness_scores)
best_index = fitness_scores.index(best_fitness)
best_chromosome = population[best_index]

print(f"Best fitness after GA: {best_fitness}")

# Function to create a DataFrame for the schedule
def create_schedule_dataframe(chromosome):
    schedule_data = []
    for day_index in range(DAYS):
        day = WEEKDAYS[day_index % 7]
        daily_schedule = chromosome[day_index * TIME_SLOTS: (day_index + 1) * TIME_SLOTS]
        for hour in range(TIME_SLOTS):
            time_label = f"{hour:02d}:00 - {hour+1:02d}:00"
            activity = daily_schedule[hour]
            schedule_data.append({
                'Day': day,
                'Hour': hour,
                'Time': time_label,
                'Activity': activity
            })
    df = pd.DataFrame(schedule_data)
    return df

# Create DataFrames for initial best and final best schedules
initial_schedule_df = create_schedule_dataframe(best_initial_chromosome)
best_schedule_df = create_schedule_dataframe(best_chromosome)

# Function to group by hours spent on each activity per day
def group_hours_by_activity(df):
    # Add a column for counting hours
    df['Hours'] = 1
    # Group by 'Day' and 'Activity' and sum the hours
    grouped_df = df.groupby(['Day', 'Activity'])['Hours'].sum().reset_index()
    # Pivot the table to have activities as columns
    pivot_df = grouped_df.pivot(index='Day', columns='Activity', values='Hours').fillna(0)
    # Reorder columns for consistency
    activity_order = ['sleep', 'commute', 'work', 'exercise', 'thesis', 'study', 'homework', 'rest']
    pivot_df = pivot_df.reindex(columns=activity_order, fill_value=0)
    return pivot_df

# Group the hours for both schedules
initial_grouped = group_hours_by_activity(initial_schedule_df)
best_grouped = group_hours_by_activity(best_schedule_df)

# Function to plot stacked bar charts
def plot_stacked_bars(grouped_df, title):
    activities = grouped_df.columns.tolist()
    days = grouped_df.index.tolist()
    data = grouped_df.values
    # Transpose data for stacking
    data = data.T

    # Colors for activities
    activity_colors = {
        'sleep': 'lightblue',
        'commute': 'grey',
        'work': 'orange',
        'exercise': 'cyan',
        'thesis': 'yellow',
        'study': 'red',
        'homework': 'pink',
        'rest': 'lightgreen'
    }

    colors = [activity_colors.get(activity, 'white') for activity in activities]

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    bottom = np.zeros(len(days))

    for i, activity in enumerate(activities):
        ax.bar(days, data[i], bottom=bottom, color=colors[i], label=activity)
        bottom += data[i]

    ax.set_ylabel('Hours')
    ax.set_title(title)
    ax.set_ylim(0, 24)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Plot the initial best schedule
plot_stacked_bars(initial_grouped, 'Initial Best Schedule - Daily Activity Allocation')

# Plot the best schedule after GA
plot_stacked_bars(best_grouped, 'Best Schedule After GA - Daily Activity Allocation')
