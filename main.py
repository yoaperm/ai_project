# first draft
import random

# Parameters
DAYS = 130  # Total days from Jan 6 to May 15
TIME_SLOTS = 24  # Hours in a day
WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# Activity dictionary with priority levels
activities = {
    'study_nlp': 4,
    'study_big_data': 3,
    'study_inf_storage': 3,
    'study_cv': 5,
    'homework': 3,
    'thesis': 5,
    'exercise': 2,
    'rest': 0,
    'sleep': 0
}

# Chromosome structure: DAYS * TIME_SLOTS genes
def create_chromosome():
    return [random.choice(list(activities.keys())) for _ in range(DAYS * TIME_SLOTS)]

# Fitness function
def fitness(chromosome):
    score = 0
    for day_index in range(DAYS):
        day = WEEKDAYS[day_index % 7]
        daily_schedule = chromosome[day_index * TIME_SLOTS: (day_index + 1) * TIME_SLOTS]
        
        # Penalty for hard study on office days
        if day in ['Tue', 'Thu']:
            score -= sum(5 for activity in daily_schedule if activity in ['study_cv', 'study_nlp'])

        # Reward for balanced schedule and rest
        if daily_schedule.count('sleep') >= 7:
            score += 10
        if 'exercise' in daily_schedule:
            score += 2
        
        # Other rules for study allocation, homework, and thesis
        score += daily_schedule.count('thesis') * 4

    return score

# Initial population
population = [create_chromosome() for _ in range(100)]
generations = 200

# GA algorithm loop
for gen in range(generations):
    population = sorted(population, key=fitness, reverse=True)
    next_generation = []
    
    # Crossover
    for _ in range(len(population) // 2):
        parent1 = random.choice(population[:20])
        parent2 = random.choice(population[:20])
        cross_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:cross_point] + parent2[cross_point:]
        child2 = parent2[:cross_point] + parent1[cross_point:]
        next_generation.extend([child1, child2])

    # Mutation
    for individual in next_generation:
        if random.random() < 0.1:
            mutate_point = random.randint(0, len(individual) - 1)
            individual[mutate_point] = random.choice(list(activities.keys()))

    population = next_generation

best_schedule = max(population, key=fitness)
print("Best schedule found:", best_schedule)


# second draf
def fitness(chromosome):
    score = 0
    for day_index in range(DAYS):
        day = get_day_of_week(day_index)
        daily_schedule = chromosome[day_index * TIME_SLOTS: (day_index + 1) * TIME_SLOTS]
        
        sleep_hours = daily_schedule.count('sleep')
        exercise_hours = daily_schedule.count('exercise')
        study_hours = daily_schedule.count('study')
        thesis_hours = daily_schedule.count('thesis')
        
        # ประเมินการนอน
        if sleep_hours >= 7:
            score += 10
        else:
            score -= 15  # เพิ่มการลงโทษ
        
        # ประเมินการออกกำลังกาย
        if exercise_hours >= 1:
            score += 5
        else:
            score -= 5
        
        # หลีกเลี่ยงการเรียนหนักในวันอังคารและพฤหัส
        if day in ['Tue', 'Thu']:
            if 'study_hard' in daily_schedule:
                score -= 10
        
        # เพิ่มคะแนนสำหรับการทำ Thesis
        if thesis_hours >= 2:
            score += 5
        
        # ตรวจสอบการซ้อนทับกับเวลาทำงานและเรียน
        if has_overlap(daily_schedule, day_index):
            score -= 20
        
        # เพิ่มคะแนนสำหรับการพักผ่อน
        if 'rest' in daily_schedule:
            score += 2
        else:
            score -= 5  # ส่งเสริมให้มีเวลาพักผ่อน

    # เพิ่มคะแนนหากทบทวนครบก่อนสอบ
    if completed_all_reviews_before_exams(chromosome):
        score += 40

    return score
