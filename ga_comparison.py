import random
import time

import pandas as pd
import streamlit as st


# Fitness function
def fitness_function(x):
    return x**2


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
        return [random.randint(0, 2**gene_length - 1) for _ in range(size)]

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
            mask = (1 << point) - 1
            child1 = (parent1 & mask) | (parent2 & ~mask)
            child2 = (parent2 & mask) | (parent1 & ~mask)
            return child1, child2
        return parent1, parent2

    def mutate(individual, gene_length):
        for bit in range(gene_length):
            if random.random() < mutation_rate:
                individual ^= 1 << bit
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


# Brute-Force Search
def brute_force_search(fitness_function, search_space):
    best_solution = None
    best_fitness = 0
    for x in search_space:
        fitness = fitness_function(x)
        if fitness > best_fitness:
            best_fitness = fitness
            best_solution = x
    return best_solution, best_fitness


# Streamlit Interface
st.title("Performance Comparison: Genetic Algorithm vs Brute-Force")

# Parameters
st.sidebar.header("Algorithm Parameters")
gene_length = st.sidebar.slider("Gene Length (bits)", 2, 50, 20)
population_size = st.sidebar.slider("Population Size (GA)", 10, 1000, 100)
generations = st.sidebar.slider("Generations (GA)", 10, 1000, 100)
mutation_rate = st.sidebar.slider("Mutation Rate (GA)", 0.0, 1.0, 0.05, 0.01)


# Run the algorithms
if st.button("Run Comparison"):
    search_space = range(2**gene_length)

    # Brute-Force Search
    start_time = time.time()
    bf_solution, bf_fitness = brute_force_search(fitness_function, search_space)
    bf_time = time.time() - start_time

    # Genetic Algorithm
    start_time = time.time()
    ga_solution, ga_fitness = genetic_algorithm(
        fitness_function, population_size, gene_length, generations, mutation_rate
    )
    ga_time = time.time() - start_time

    # Results
    st.subheader("Results")

    data = pd.DataFrame(
        {
            "Algorithm": ["Brute-Force", "Genetic Algorithm"],
            "Execution Time (s)": [bf_time, ga_time],
        }
    )
    st.subheader("Execution Time Comparison")
    st.bar_chart(data.set_index("Algorithm"))
    st.write(data)

    st.write("### Brute-Force Search")
    st.write(f"Best Solution: {bf_solution}, Fitness: {bf_fitness}")
    st.write(f"Execution Time: {bf_time:.4f} seconds")

    st.write("### Genetic Algorithm")
    st.write(f"Best Solution: {ga_solution}, Fitness: {ga_fitness}")
    st.write(f"Execution Time: {ga_time:.4f} seconds")

    # Comparison
    st.subheader("Performance Comparison")
    st.write(f"**Execution Time Ratio (GA/Brute-Force):** {ga_time/bf_time:.2f}")
    st.write("**Efficiency:**")
    if bf_fitness == ga_fitness:
        st.success("Both algorithms found the optimal solution!")
    elif bf_fitness > ga_fitness:
        st.warning("Brute-Force found a better solution.")
    else:
        st.success("Genetic Algorithm outperformed Brute-Force.")
