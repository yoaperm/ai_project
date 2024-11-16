import random
import numpy as np

# จำนวนวันทั้งหมด (6 ม.ค. 2568 - 15 พ.ค. 2568)
total_days = 130  # คุณสามารถคำนวณจำนวนวันจริงได้
time_slots = 24

# กิจกรรมที่เป็นไปได้
activities = ['sleep', 'work', 'nlp_course', 'other_courses', 'homework', 'thesis', 'exercise', 'rest']
activity_indices = {activity: idx for idx, activity in enumerate(activities)}

num_genes = total_days * time_slots

# เริ่มต้นเวกเตอร์ความน่าจะเป็น
prob_vector = np.full((num_genes, len(activities)), 1 / len(activities))

# ฟิตเนสฟังก์ชัน
def fitness(chromosome):
    score = 0
    daily_schedules = np.reshape(chromosome, (total_days, time_slots))
    
    for day_index in range(total_days):
        day_schedule = daily_schedules[day_index]
        activity_counts = {activity: np.count_nonzero(day_schedule == activity_indices[activity]) for activity in activities}
        
        # นอนหลับ
        sleep_hours = activity_counts['sleep']
        if sleep_hours >= 7:
            score += 10
        else:
            score -= 10
        
        # ทำงาน
        work_hours = activity_counts['work']
        if work_hours != 8:
            score -= abs(work_hours - 8) * 5
        
        # หลีกเลี่ยงการเรียนวิชาที่ยากในวันอังคารและพฤหัส
        weekday = (6 + day_index) % 7  # 0=จันทร์, 1=อังคาร, ..., 6=อาทิตย์
        if weekday in [1, 3]:  # อังคารและพฤหัส
            nlp_hours = activity_counts['nlp_course']
            if nlp_hours > 0:
                score -= nlp_hours * 5
        
        # ออกกำลังกาย
        exercise_hours = activity_counts['exercise']
        if exercise_hours > 0:
            score += 5
        
        # ทำ Thesis
        thesis_hours = activity_counts['thesis']
        score += thesis_hours * 2
        
        # พักผ่อน
        rest_hours = activity_counts['rest']
        score += rest_hours
        
        # ตรวจสอบเวลารวม
        total_hours = sum(activity_counts.values())
        if total_hours != 24:
            score -= abs(24 - total_hours) * 10
    
    return score

# สร้างโครโมโซม
def generate_chromosome(prob_vector):
    chromosome = []
    for probs in prob_vector:
        activity = np.random.choice(activities, p=probs)
        chromosome.append(activity_indices[activity])
    return np.array(chromosome)

# อัพเดตเวกเตอร์ความน่าจะเป็น
def update_probability_vector(prob_vector, winner, loser, population_size):
    for i in range(len(prob_vector)):
        winner_gene = winner[i]
        loser_gene = loser[i]
        
        if winner_gene != loser_gene:
            prob_vector[i][winner_gene] += 1.0 / population_size
            prob_vector[i][loser_gene] -= 1.0 / population_size
            prob_vector[i] = np.clip(prob_vector[i], 0.0, 1.0)
            prob_vector[i] /= np.sum(prob_vector[i])

# วนลูปหลัก
population_size = 50
max_iterations = 1000
desired_max_score = 10000  # กำหนดคะแนนที่ต้องการ

for iteration in range(max_iterations):
    chrom1 = generate_chromosome(prob_vector)
    chrom2 = generate_chromosome(prob_vector)
    
    fit1 = fitness(chrom1)
    fit2 = fitness(chrom2)
    
    if fit1 > fit2:
        winner, loser = chrom1, chrom2
        best_fit = fit1
    else:
        winner, loser = chrom2, chrom1
        best_fit = fit2
    
    update_probability_vector(prob_vector, winner, loser, population_size)
    
    if best_fit >= desired_max_score:
        print(f"Optimal schedule found at iteration {iteration}")
        best_chromosome = winner
        break
else:
    print("Max iterations reached without finding optimal schedule")
    best_chromosome = winner  # หรือเลือกโครโมโซมที่ดีที่สุดจากการวนลูปทั้งหมด

# แสดงตารางเวลาที่ดีที่สุด
def display_schedule(chromosome):
    daily_schedules = np.reshape(chromosome, (total_days, time_slots))
    for day_index in range(total_days):
        day_schedule = daily_schedules[day_index]
        day_activities = [activities[gene] for gene in day_schedule]
        date = f"Day {day_index + 1}"
        print(f"{date}: {day_activities}")

# เรียกใช้ฟังก์ชันแสดงตารางเวลา
display_schedule(best_chromosome)
