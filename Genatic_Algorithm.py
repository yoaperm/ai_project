import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
import random
import pandas as pd

# Constants
HOURS_IN_DAY = 24
MIN_SLEEP_HOURS = 7
MAX_WORK_STUDY_HOURS = 12

# Updated list of activities
ACTIVITIES = [
    'Work', 'Study', 'Rest/Nap', 'Sleep', 'Exercise',
    'Meals', 'Leisure', 'Socializing', 'Personal Care', 'Commuting'
]
NUM_ACTIVITIES = len(ACTIVITIES)

# User Preferences (weights sum to 1)
USER_PREFERENCES = {
    'Work': 0.2,
    'Study': 0.15,
    'Rest/Nap': 0.05,
    'Sleep': 0.25,
    'Exercise': 0.1,
    'Meals': 0.05,
    'Leisure': 0.05,
    'Socializing': 0.05,
    'Personal Care': 0.05,
    'Commuting': 0.05
}

# Tension weights (lower is less tension)
TENSION_WEIGHTS = {
    'Work': 8,
    'Study': 6,
    'Rest/Nap': 2,
    'Sleep': 1,
    'Exercise': 3,
    'Meals': 2,
    'Leisure': 1,
    'Socializing': 2,
    'Personal Care': 1,
    'Commuting': 5
}

# Productivity weights
PRODUCTIVITY_WEIGHTS = {
    'Work': 1.5,
    'Study': 1.2,
    'Rest/Nap': 0.5,
    'Sleep': 0.8,
    'Exercise': 1.0,
    'Meals': 0.2,
    'Leisure': 0.3,
    'Socializing': 0.5,
    'Personal Care': 0.1,
    'Commuting': 0.2
}

# Fitness Function Weights (maximize productivity, minimize tension)
creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))  # Maximize productivity, minimize tension
creator.create("Individual", list, fitness=creator.FitnessMulti)

toolbox = base.Toolbox()

# Attribute generator: Generates a random hour allocation for each activity
def random_hour_allocation():
    allocation = np.random.dirichlet(np.ones(NUM_ACTIVITIES)) * HOURS_IN_DAY
    allocation = [round(hour) for hour in allocation]
    # Adjust the total hours to exactly HOURS_IN_DAY
    total_hours = sum(allocation)
    while total_hours != HOURS_IN_DAY:
        diff = HOURS_IN_DAY - total_hours
        idx = random.randrange(NUM_ACTIVITIES)
        allocation[idx] = max(0, allocation[idx] + diff)
        total_hours = sum(allocation)
    return allocation

toolbox.register("individual", tools.initIterate, creator.Individual, random_hour_allocation)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Modify the evaluate function to add constraints for essential activities
def evaluate(individual):
    # Convert individual to a dict for easier handling
    schedule = dict(zip(ACTIVITIES, individual))
    total_hours = sum(individual)

    # Soft constraints penalties
    penalties = 0

    # Constraint: Total hours should equal HOURS_IN_DAY
    if total_hours != HOURS_IN_DAY:
        penalties += abs(HOURS_IN_DAY - total_hours) * 10

    # Constraint: Minimum sleep hours
    if schedule['Sleep'] < MIN_SLEEP_HOURS:
        penalties += (MIN_SLEEP_HOURS - schedule['Sleep']) * 15

    # Constraint: Max combined work and study hours
    if (schedule['Work'] + schedule['Study']) > MAX_WORK_STUDY_HOURS:
        penalties += ((schedule['Work'] + schedule['Study']) - MAX_WORK_STUDY_HOURS) * 10

    # New constraints: Ensure a minimum of 1 hour for Meals
    if schedule['Meals'] < 1:
        penalties += (1 - schedule['Meals']) * 20  # Apply a high penalty for missing meal hours

    # Optional: Minimum hours for Personal Care and Leisure
    if schedule['Personal Care'] < 1:
        penalties += (1 - schedule['Personal Care']) * 10
    if schedule['Leisure'] < 1:
        penalties += (1 - schedule['Leisure']) * 10

    # Total tension
    total_tension = sum(schedule[activity] * TENSION_WEIGHTS[activity] for activity in ACTIVITIES)

    # Productivity score
    productivity = sum(schedule[activity] * PRODUCTIVITY_WEIGHTS[activity] for activity in ACTIVITIES)

    # Adjust productivity and tension based on penalties
    adjusted_productivity = productivity - penalties
    adjusted_tension = total_tension + penalties

    return adjusted_productivity, adjusted_tension


def mutate_individual(individual):
    idx = random.randrange(len(individual))
    change = random.choice([-1, 1]) * random.randint(1, 2)
    individual[idx] = max(0, individual[idx] + change)

    # Ensure total hours remain within the limit
    total_hours = sum(individual)
    if total_hours > HOURS_IN_DAY:
        diff = total_hours - HOURS_IN_DAY
        individual[idx] = max(0, individual[idx] - diff)
    elif total_hours < HOURS_IN_DAY:
        diff = HOURS_IN_DAY - total_hours
        individual[idx] = individual[idx] + diff

    # Ensure no negative hours
    individual[idx] = max(0, individual[idx])

    return individual,

toolbox.register("mate", tools.cxUniform, indpb=0.5)
toolbox.register("mutate", mutate_individual)
toolbox.register("select", tools.selNSGA2)
toolbox.register("evaluate", evaluate)

def main():
    population = toolbox.population(n=300)
    NGEN = 150
    MU = 300
    LAMBDA = 400
    CXPB = 0.7
    MUTPB = 0.2

    # Save an initial schedule for comparison
    initial_individual = population[0]
    initial_schedule = dict(zip(ACTIVITIES, initial_individual))

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    hof = tools.ParetoFront()

    algorithms.eaMuPlusLambda(population, toolbox, mu=MU, lambda_=LAMBDA,
                              cxpb=CXPB, mutpb=MUTPB, ngen=NGEN,
                              stats=stats, halloffame=hof, verbose=True)

    return population, stats, hof, initial_schedule

if __name__ == "__main__":
    population, stats, hof, initial_schedule = main()

    # Extract the best individual
    best_individual = tools.selBest(population, k=1)[0]
    best_schedule = dict(zip(ACTIVITIES, best_individual))

    print("\nInitial Schedule:")
    for activity, hours in initial_schedule.items():
        print(f"{activity}: {hours} hours")

    print("\nBest Schedule Found:")
    for activity, hours in best_schedule.items():
        print(f"{activity}: {hours} hours")

    # Function to add data labels to bar charts
    def add_data_labels(ax, rects):
        for rect in rects:
            height = rect.get_height()
            if height > 0:
                ax.annotate(f'{int(height)}',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

    # Enhanced bar chart visualization function
    def plot_comparison_bar_chart(initial_schedule, best_schedule, activities):
        x = np.arange(len(activities))
        width = 0.35

        fig, ax = plt.subplots(figsize=(12, 6))
        rects1 = ax.bar(x - width/2, [initial_schedule[activity] for activity in activities], width, label='Initial Schedule', color='lightblue')
        rects2 = ax.bar(x + width/2, [best_schedule[activity] for activity in activities], width, label='Best Schedule', color='orange')

        ax.set_xlabel('Activities')
        ax.set_ylabel('Hours Allocated')
        ax.set_title('Comparison of Initial and Best Schedules')
        ax.set_xticks(x)
        ax.set_xticklabels(activities)
        ax.legend()
        plt.grid(True)
        add_data_labels(ax, rects1)
        add_data_labels(ax, rects2)
        plt.tight_layout()
        plt.show()

    # Function to plot side-by-side Gantt charts
    def plot_comparison_gantt(initial_schedule, best_schedule, activities):
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))

        for ax, schedule, title in zip(axes, [initial_schedule, best_schedule], ['Initial Schedule', 'Best Schedule']):
            schedule_data = []
            start_time = 0
            for activity in activities:
                finish_time = start_time + schedule[activity]
                if finish_time > start_time:
                    schedule_data.append({
                        'Activity': activity,
                        'Start': start_time,
                        'Finish': finish_time
                    })
                start_time = finish_time

            df = pd.DataFrame(schedule_data)

            for idx, row in df.iterrows():
                ax.barh(row['Activity'], row['Finish'] - row['Start'], left=row['Start'], color=plt.cm.Paired(idx / len(df)))
            
            ax.set_xlabel('Time (Hours)')
            ax.set_xlim(0, HOURS_IN_DAY)
            ax.set_title(title)
            ax.invert_yaxis()  # Invert y-axis to have the first activity at the top
            ax.grid(True)
        
        plt.tight_layout()
        plt.show()

    # Call the enhanced visualization functions
    plot_comparison_bar_chart(initial_schedule, best_schedule, ACTIVITIES)
    plot_comparison_gantt(initial_schedule, best_schedule, ACTIVITIES)

    # Pareto Front Visualization
    pareto_points = np.array([ind.fitness.values for ind in hof])
    plt.figure(figsize=(10, 6))
    plt.scatter(
        pareto_points[:, 1],  # Tension on X-axis
        pareto_points[:, 0],  # Productivity on Y-axis
        c='blue',
        label='Pareto Front'
    )
    plt.xlabel('Total Tension (Lower is better)')
    plt.ylabel('Productivity (Higher is better)')
    plt.title('Pareto Front of Optimized Schedules')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

