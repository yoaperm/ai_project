from mv_cga import MultiValuedCompactGeneticAlgorithm

# Parameters for the scheduling problem
DAYS = 7  # Total days from Jan 6 to May 15
TIME_SLOTS = 24  # Hours in a day
ACTIVITIES = [
    "study_nlp",
    "study_big_data",
    "study_inf_storage",
    "study_cv",
    "homework",
    "thesis",
    "exercise",
    "rest",
    "sleep",
]
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

activity_priorities = {
    "study_nlp": 4,
    "study_big_data": 3,
    "study_inf_storage": 3,
    "study_cv": 5,
    "homework": 3,
    "thesis": 5,
    "exercise": 2,
    "rest": 0,
    "sleep": 0,
}


# Fitness function for the scheduling problem
def fitness(chromosome):
    score = 0
    for day_index in range(DAYS):
        day = WEEKDAYS[day_index % 7]
        daily_schedule = [
            ACTIVITIES[gene]
            for gene in chromosome[
                day_index * TIME_SLOTS : (day_index + 1) * TIME_SLOTS
            ]
        ]

        sleep_hours = daily_schedule.count("sleep")
        exercise_hours = daily_schedule.count("exercise")
        thesis_hours = daily_schedule.count("thesis")

        # Evaluate sleep
        if sleep_hours >= 7:
            score += 10
        else:
            score -= 15

        # Evaluate exercise
        if exercise_hours >= 1:
            score += 5
        else:
            score -= 5

        # Avoid hard study on certain days
        if day in ["Tue", "Thu"]:
            if "study_cv" in daily_schedule or "study_nlp" in daily_schedule:
                score -= 10

        # Reward thesis work
        score += thesis_hours * 4

        # Encourage rest
        if "rest" in daily_schedule:
            score += 2
        else:
            score -= 5

    return score


# MV-cGA parameters
chromosome_length = DAYS * TIME_SLOTS  # Total hours in the scheduling period
num_values = len(ACTIVITIES)  # Number of different activities
population_size = 50  # Virtual population size
max_generations = 2000  # Number of generations
learning_rate = 0.02  # Custom learning rate

# Run the MV-cGA
mv_cga = MultiValuedCompactGeneticAlgorithm(
    chromosome_length,
    num_values,
    population_size,
    max_generations,
    fitness,
    learning_rate,
)
print("Initial provability matrix:", mv_cga.probability_matrix)
best_chromosome, probability_matrix = mv_cga.run()

# Decode and display the best chromosome
best_schedule = [ACTIVITIES[gene] for gene in best_chromosome]
print("Best schedule found:", best_schedule)
