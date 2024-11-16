import numpy as np


class MultiValuedCompactGeneticAlgorithm:
    def __init__(
        self,
        chromosome_length,
        num_values,
        population_size,
        max_generations,
        fitness_function,
        learning_rate=None,
    ):
        """
        Initialize the Multi-Valued Compact Genetic Algorithm (MV-cGA).

        Args:
            chromosome_length (int): Length of the chromosome.
            num_values (int): Number of possible values each gene can take (e.g., 3 for {0, 1, 2}).
            population_size (int): Virtual population size for the cGA.
            max_generations (int): Maximum number of generations to run the algorithm.
            fitness_function (function): Function to evaluate fitness of a chromosome.
            learning_rate (float): Learning rate for probability matrix updates. If None, defaults to 1 / population_size.
        """
        self.chromosome_length = chromosome_length
        self.num_values = num_values
        self.population_size = population_size
        self.max_generations = max_generations
        self.fitness_function = fitness_function
        self.learning_rate = (
            learning_rate if learning_rate is not None else 1 / population_size
        )
        self.probability_matrix = np.full(
            (chromosome_length, num_values), 1 / num_values
        )

    def generate_chromosome(self):
        """Generate a chromosome based on the probability matrix."""
        chromosome = []
        for i in range(self.chromosome_length):
            value = np.random.choice(self.num_values, p=self.probability_matrix[i])
            chromosome.append(value)
        return chromosome

    def update_probability_matrix(self, winner, loser):
        """Update the probability matrix towards the winner chromosome."""
        for i in range(self.chromosome_length):
            if winner[i] != loser[i]:
                # Decrease probability for the loser's value
                self.probability_matrix[i, loser[i]] -= self.learning_rate
                # Increase probability for the winner's value
                self.probability_matrix[i, winner[i]] += self.learning_rate

                # Ensure probabilities stay within bounds [0, 1] and re-normalize
                self.probability_matrix[i] = np.clip(self.probability_matrix[i], 0, 1)
                self.probability_matrix[i] /= self.probability_matrix[i].sum()

    def run(self):
        """Run the MV-cGA for the specified number of generations."""
        for generation in range(self.max_generations):
            # Generate two chromosomes
            chromosome_a = self.generate_chromosome()
            chromosome_b = self.generate_chromosome()

            # Evaluate fitness
            fitness_a = self.fitness_function(chromosome_a)
            fitness_b = self.fitness_function(chromosome_b)

            # Determine winner and loser
            if fitness_a > fitness_b:
                winner, loser = chromosome_a, chromosome_b
            else:
                winner, loser = chromosome_b, chromosome_a

            # Update probability matrix towards the winner
            self.update_probability_matrix(winner, loser)

        # Return final probability matrix and best chromosome found
        best_chromosome = self.generate_chromosome()
        return best_chromosome, self.probability_matrix


# Example usage
if __name__ == "__main__":
    # Define a sample fitness function for demonstration
    def fitness_function(chromosome):
        return sum(chromosome)  # Example: maximize the sum of the chromosome values

    # Parameters
    chromosome_length = 8 * 24
    num_values = 8
    population_size = 50
    max_generations = 2000
    learning_rate = 0.02

    # Create and run the MV-cGA
    mv_cga = MultiValuedCompactGeneticAlgorithm(
        chromosome_length,
        num_values,
        population_size,
        max_generations,
        fitness_function,
        learning_rate,
    )
    print("Initial probability vector:", mv_cga.probability_matrix)
    best_chromosome, probability_matrix = mv_cga.run()

    print("Best chromosome found:", best_chromosome, sum(best_chromosome))
    print("Final probability matrix:", probability_matrix)
