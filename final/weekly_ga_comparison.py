import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Parameters
DAYS = 7  # Number of days in the schedule
TIME_SLOTS = 24  # Hours in a day
WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# Activities
# activities = [
#     'sleep',            # Sleeping
#     'eat',              # Eating
#     'personal_care',    # Personal care
#     'commute',          # Commuting
#     'work_home',        # Work from home
#     'work_office',      # Work at office
#     'class_online',     # Online class
#     'class_university', # University class
#     'thesis_homework',  # Thesis/Homework
#     'rest',             # Resting
#     'exercise',         # Exercising
#     'socializing',      # Socializing
#     'leisure',          # Leisure activities
# ]

# Measure time and space for Standard GA
tracemalloc.start()
start_time = time.time()

# Define mandatory hours
work_hours = 8
class_hours = 6
sleep_min_hours = 6

# Time constraints
sleep_time = list(range(22, 24)) + list(range(0, 6))  # Preferred sleep time
meal_times = [7, 12, 18]  # Breakfast, Lunch, Dinner

# Office days and remote days
office_days = ['Tue', 'Thu']
remote_days = ['Mon', 'Wed', 'Fri']

# Chromosome structure: DAYS * TIME_SLOTS genes
def create_chromosome():
    chromosome = []
    for day_index in range(DAYS):
        day = WEEKDAYS[day_index % 7]
        daily_schedule = [''] * TIME_SLOTS

        # Initialize with sleep during preferred sleep time
        for hour in sleep_time:
            daily_schedule[hour] = 'sleep'

        # Schedule personal care (e.g., showering) once per day
        for hour in range(TIME_SLOTS):
            if daily_schedule[hour] == '':
                daily_schedule[hour] = 'personal_care'
                break

        # Schedule meals at meal times
        for hour in meal_times:
            if daily_schedule[hour] == '':
                daily_schedule[hour] = 'eat'
            else:
                # Find the next available slot
                for h in range(TIME_SLOTS):
                    if daily_schedule[h] == '':
                        daily_schedule[h] = 'eat'
                        break

        # Schedule mandatory activities
        if day in remote_days:
            # Work from home
            work_count = 0
            for hour in range(TIME_SLOTS):
                if daily_schedule[hour] == '' and work_count < work_hours:
                    daily_schedule[hour] = 'work_home'
                    work_count += 1
        elif day in office_days:
            # Commute and work at office
            commute_hours = 2  # Total commute time per day
            commute_count = 0
            work_count = 0
            for hour in range(TIME_SLOTS):
                if daily_schedule[hour] == '' and commute_count < 1:
                    daily_schedule[hour] = 'commute'
                    commute_count += 1
                elif daily_schedule[hour] == '' and work_count < work_hours:
                    daily_schedule[hour] = 'work_office'
                    work_count += 1
                elif daily_schedule[hour] == '' and commute_count < 2:
                    daily_schedule[hour] = 'commute'
                    commute_count += 1
        elif day == 'Sat':
            # Online class
            class_count = 0
            for hour in range(TIME_SLOTS):
                if daily_schedule[hour] == '' and class_count < class_hours:
                    daily_schedule[hour] = 'class_online'
                    class_count += 1
        elif day == 'Sun':
            # Commute and class at university
            commute_hours = 2  # Total commute time
            commute_count = 0
            class_count = 0
            for hour in range(TIME_SLOTS):
                if daily_schedule[hour] == '' and commute_count < 1:
                    daily_schedule[hour] = 'commute'
                    commute_count += 1
                elif daily_schedule[hour] == '' and class_count < class_hours:
                    daily_schedule[hour] = 'class_university'
                    class_count += 1
                elif daily_schedule[hour] == '' and commute_count < 2:
                    daily_schedule[hour] = 'commute'
                    commute_count += 1

        # Fill the rest of the day with optional activities
        for hour in range(TIME_SLOTS):
            if daily_schedule[hour] == '':
                optional_activities = [
                    'thesis_homework',
                    'rest',
                    'exercise',
                    'socializing',
                    'leisure',
                    'sleep'  # Additional sleep if needed
                ]
                daily_schedule[hour] = random.choice(optional_activities)

        chromosome.extend(daily_schedule)
    return chromosome

# Fitness function with penalties
def fitness(chromosome):
    score = 0
    total_work_hours_week = 0
    total_sleep_hours_week = 0
    did_beneficial_activities = False

    for day_index in range(DAYS):
        day = WEEKDAYS[day_index % 7]
        daily_schedule = chromosome[day_index * TIME_SLOTS: (day_index + 1) * TIME_SLOTS]

        # Count activities
        sleep_hours_count = daily_schedule.count('sleep')
        work_home_hours = daily_schedule.count('work_home')
        work_office_hours = daily_schedule.count('work_office')
        work_hours_count = work_home_hours + work_office_hours
        class_online_hours = daily_schedule.count('class_online')
        class_university_hours = daily_schedule.count('class_university')
        class_hours_count = class_online_hours + class_university_hours
        eat_count = daily_schedule.count('eat')
        exercise_hours = daily_schedule.count('exercise')
        rest_hours = daily_schedule.count('rest')
        thesis_hours = daily_schedule.count('thesis_homework')

        total_work_hours_week += work_hours_count
        total_sleep_hours_week += sleep_hours_count

        # Penalties and rewards
        # 1. Work hours
        if day in remote_days + office_days:
            if work_hours_count < 8:
                score -= 1000 * (8 - work_hours_count)
            if work_hours_count == 0:
                score -= float('inf')  # Dead individual
            if day in office_days:
                commute_count = daily_schedule.count('commute')
                if commute_count < 2:
                    score -= 500 * (2 - commute_count)

        # 2. Class hours
        if day in ['Sat', 'Sun']:
            if class_hours_count < 6:
                score -= 100 * (6 - class_hours_count)
            if day == 'Sun':
                commute_count = daily_schedule.count('commute')
                if commute_count < 2:
                    score -= 50 * (2 - commute_count)

        # 3. Sleep hours
        if sleep_hours_count < sleep_min_hours:
            score -= 100 * (sleep_min_hours - sleep_hours_count)

        # 4. Eating
        if eat_count < 3:
            score -= 50 * (3 - eat_count)

        # 5. Beneficial activities
        if exercise_hours > 0 or rest_hours > 0:
            did_beneficial_activities = True
            score += 10 * (exercise_hours + rest_hours)
        else:
            score -= 20  # Penalty for not doing beneficial activities

        # 6. Personal care
        if 'personal_care' not in daily_schedule:
            score -= 30  # Penalty for skipping personal care

    # Weekly penalties
    if total_work_hours_week < 40:
        score -= 1000 * (40 - total_work_hours_week)
    if total_work_hours_week == 0:
        score -= float('inf')  # Dead individual

    # Total sleep hours in the week
    if total_sleep_hours_week < sleep_min_hours * DAYS:
        score -= 100 * (sleep_min_hours * DAYS - total_sleep_hours_week)

    return score

# Genetic Algorithm parameters
population_size = 100
generations = 150
mutation_rate = 0.1

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

    # Selection (Tournament Selection)
    selected_population = []
    for _ in range(population_size):
        contenders = random.sample(population, 3)
        contender_fitness = [fitness(chrom) for chrom in contenders]
        winner = contenders[contender_fitness.index(max(contender_fitness))]
        selected_population.append(winner)

    # Crossover
    next_generation = []
    while len(next_generation) < population_size:
        parent1 = random.choice(selected_population)
        parent2 = random.choice(selected_population)
        if parent1 != parent2:
            cross_point = random.randint(1, len(parent1) - 2)
            child1 = parent1[:cross_point] + parent2[cross_point:]
            child2 = parent2[:cross_point] + parent1[cross_point:]
            next_generation.extend([child1, child2])

    # Mutation
    for individual in next_generation:
        if random.random() < mutation_rate:
            mutate_point = random.randint(0, len(individual) - 1)
            day = WEEKDAYS[(mutate_point // TIME_SLOTS) % 7]
            hour = mutate_point % TIME_SLOTS
            # Apply mutation considering the constraints
            if day in remote_days + office_days and individual[mutate_point] in ['work_home', 'work_office', 'commute']:
                continue  # Do not mutate mandatory work hours
            if day in ['Sat', 'Sun'] and individual[mutate_point] in ['class_online', 'class_university', 'commute']:
                continue  # Do not mutate mandatory class hours
            if individual[mutate_point] == 'sleep' and hour in sleep_time:
                continue  # Do not mutate sleep during sleep time
            # Otherwise, mutate to a random optional activity
            optional_activities = [
                'thesis_homework',
                'rest',
                'exercise',
                'socializing',
                'leisure',
                'sleep',
                'eat',
                'personal_care'
            ]
            individual[mutate_point] = random.choice(optional_activities)

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
        'eat': 'orange',
        'personal_care': 'pink',
        'commute': 'grey',
        'work_home': 'green',
        'work_office': 'darkgreen',
        'class_online': 'purple',
        'class_university': 'indigo',  # Updated color
        'thesis_homework': 'yellow',
        'rest': 'lightgreen',
        'exercise': 'cyan',
        'socializing': 'red',
        'leisure': 'gold'
    }

    colors = [activity_colors.get(activity, 'white') for activity in activities]

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 7))

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





end_time = time.time()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"Best fitness after GA: {best_fitness}")
print(f"Time taken by Standard GA: {end_time - start_time:.2f} seconds")
print(f"Memory usage by Standard GA: Current = {current / 10**6:.2f} MB; Peak = {peak / 10**6:.2f} MB")