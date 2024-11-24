import random
import time
import tracemalloc

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from mv_cga import MultiValuedCompactGeneticAlgorithm

# Initialize or load history
if "history" not in st.session_state:
    st.session_state.history = []


# Fitness function (handles both binary and multi-valued chromosome representations)
def fitness_function(chromosome):
    if isinstance(chromosome, list):  # GA binary representation (list of bits)
        return sum(chromosome)  # count '1's as a fitness metric
    else:  # MV-cGA multi-valued representation
        return sum(chromosome)  # sum as a fitness metric


# Genetic Algorithm Implementation
def genetic_algorithm(
    fitness_function,
    population_size,
    gene_length,
    generations,
    mutation_rate=0.01,
    crossover_rate=0.7,
):
    def initialize_population(size, gene_length):
        return [
            [random.choice([0, 1]) for _ in range(gene_length)] for _ in range(size)
        ]

    def selection(population, fitnesses):
        selected = []
        for _ in range(len(population)):
            i1, i2 = random.sample(range(len(population)), 2)
            winner = i1 if fitnesses[i1] > fitnesses[i2] else i2
            selected.append(population[winner])
        return selected

    def crossover(parent1, parent2, gene_length):
        if random.random() < crossover_rate:
            point = random.randint(1, gene_length - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        return parent1, parent2

    def mutate(individual, gene_length):
        for bit in range(gene_length):
            if random.random() < mutation_rate:
                individual[bit] ^= 1  # Flip the bit
        return individual

    # Initialize population
    population = initialize_population(population_size, gene_length)
    best_fitness = 0
    best_individual = None

    for generation in range(generations):
        fitnesses = [fitness_function(ind) for ind in population]
        if max(fitnesses) > best_fitness:
            best_fitness = max(fitnesses)
            best_individual = population[fitnesses.index(best_fitness)]

        population = selection(population, fitnesses)
        new_population = []
        for i in range(0, len(population), 2):
            p1 = population[i]
            p2 = population[i + 1] if i + 1 < len(population) else population[0]
            c1, c2 = crossover(p1, p2, gene_length)
            new_population.extend([c1, c2])
        population = [mutate(ind, gene_length) for ind in new_population]

    return best_individual, best_fitness


# Streamlit Interface
st.title("Performance and Memory Comparison: GA vs MV-cGA")

# Parameters
st.sidebar.header("Algorithm Parameters")
gene_length = st.sidebar.slider("Gene Length (bits for GA)", 2, 1000, 20)
population_size = st.sidebar.slider("Population Size", 10, 1000, 100)
generations = st.sidebar.slider("Generations", 10, 3000, 100)
mutation_rate = st.sidebar.slider("Mutation Rate (GA)", 0.0, 1.0, 0.05, 0.01)

# MV-cGA Parameters
num_values = st.sidebar.slider("Number of Values per Gene (MV-cGA)", 2, 10, 2)
learning_rate = st.sidebar.slider("Learning Rate (MV-cGA)", 0.001, 0.1, 0.02)


# Run the algorithms
if st.button("Run Comparison"):
    # GA Memory Usage
    tracemalloc.start()
    ga_start_time = time.time()
    ga_solution, ga_fitness = genetic_algorithm(
        fitness_function, population_size, gene_length, generations, mutation_rate
    )
    ga_time = time.time() - ga_start_time
    _, ga_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # MV-cGA Memory Usage
    mv_cga = MultiValuedCompactGeneticAlgorithm(
        chromosome_length=gene_length,
        num_values=num_values,
        population_size=population_size,
        max_generations=generations,
        fitness_function=fitness_function,
        learning_rate=learning_rate,
    )
    tracemalloc.start()
    cga_start_time = time.time()
    cga_solution, cga_probability_matrix = mv_cga.run()
    cga_fitness = fitness_function(cga_solution)
    cga_time = time.time() - cga_start_time
    _, cga_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Store current run results in history
    st.session_state.history.append(
        {
            "Gene Length": gene_length,
            "Population Size": population_size,
            "Generations": generations,
            "Mutation Rate": mutation_rate,
            "GA Best Solution": ga_solution,
            "GA Fitness": ga_fitness,
            "GA Time (s)": ga_time,
            "GA Memory (KiB)": ga_memory / 1024,
            "MV-cGA Best Solution": cga_solution,
            "MV-cGA Fitness": cga_fitness,
            "MV-cGA Time (s)": cga_time,
            "MV-cGA Memory (KiB)": cga_memory / 1024,
            "Time Ratio (MV-cGA/GA)": cga_time / ga_time,
            "Memory Ratio (MV-cGA/GA)": cga_memory / ga_memory,
        }
    )

# Display results and history
if st.session_state.history:
    st.subheader("Current Run and History of Past Runs")

    # Create DataFrame to display history
    history_df = pd.DataFrame(st.session_state.history)
    st.write(history_df)

    # Prepare data for matplotlib double bar chart
    runs = range(1, len(st.session_state.history) + 1)
    ga_times = history_df["GA Time (s)"]
    cga_times = history_df["MV-cGA Time (s)"]
    ga_memories = history_df["GA Memory (KiB)"]
    cga_memories = history_df["MV-cGA Memory (KiB)"]

    # Plotting with matplotlib
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    width = 0.35  # Width of the bars

    # Execution Time Comparison
    ax1.bar([r - width / 2 for r in runs], ga_times, width, label="GA")
    ax1.bar([r + width / 2 for r in runs], cga_times, width, label="MV-cGA")
    ax1.set_xlabel("Run")
    ax1.set_ylabel("Execution Time (s)")
    ax1.set_title("Execution Time Comparison")
    ax1.set_xticks(runs)
    ax1.legend()

    # Memory Usage Comparison
    ax2.bar([r - width / 2 for r in runs], ga_memories, width, label="GA")
    ax2.bar([r + width / 2 for r in runs], cga_memories, width, label="MV-cGA")
    ax2.set_xlabel("Run")
    ax2.set_ylabel("Memory Usage (KiB)")
    ax2.set_title("Memory Usage Comparison")
    ax2.set_xticks(runs)
    ax2.legend()

    # Display matplotlib chart in Streamlit
    st.pyplot(fig)

    # Display detailed history for each run
    st.write("**Run Details**:")
    for i, run in enumerate(st.session_state.history, 1):
        st.write(f"### Run {i}")
        st.write(f"Gene Length: {run['Gene Length']}")
        st.write(f"Population Size: {run['Population Size']}")
        st.write(f"Generations: {run['Generations']}")
        st.write(f"Mutation Rate (GA): {run['Mutation Rate']}")
        st.write(
            f"GA - Best Solution: {run['GA Best Solution']}, Fitness: {run['GA Fitness']}, Time: {run['GA Time (s)']:.4f} s, Memory: {run['GA Memory (KiB)']:.2f} KiB"
        )
        st.write(
            f"MV-cGA - Best Solution: {run['MV-cGA Best Solution']}, Fitness: {run['MV-cGA Fitness']}, Time: {run['MV-cGA Time (s)']:.4f} s, Memory: {run['MV-cGA Memory (KiB)']:.2f} KiB"
        )
        st.write(f"Time Ratio (MV-cGA/GA): {run['Time Ratio (MV-cGA/GA)']:.2f}")
        st.write(f"Memory Ratio (MV-cGA/GA): {run['Memory Ratio (MV-cGA/GA)']:.2f}")
        st.write("---")
