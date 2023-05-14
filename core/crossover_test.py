import random


def crossover(chromosomes):
    """
    Perform crossover on a list of chromosomes.

    Args:
    - chromosomes: list of chromosomes, where each chromosome is a list of genes

    Returns:
    - offspring: list of new chromosomes generated through crossover
    """

    num_chromosomes = len(chromosomes)
    num_genes = len(chromosomes[0])
    offspring = []

    # Perform crossover on pairs of chromosomes
    for i in range(0, num_chromosomes, 2):
        # Choose a random crossover point
        crossover_point = random.randint(1, num_genes - 1)

        # Perform crossover at the selected point
        parent1 = chromosomes[i]
        parent2 = chromosomes[i + 1]
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]

        # Ensure that all genes in the offspring sum to 1
        normalize(child1)
        normalize(child2)

        # Add the new chromosomes to the offspring list
        offspring.append(child1)
        offspring.append(child2)

    return offspring


def normalize(chromosome):
    """
    Normalize a chromosome so that all genes sum to 1.
    """

    total = sum(chromosome)
    for i in range(len(chromosome)):
        chromosome[i] /= total


chromosomes = [[0.1, 0.2, 0.3, 0.2, 0.2, 0.1], [0.2, 0.2, 0.1, 0.1, 0.2, 0.3], [0.1, 0.3, 0.1, 0.1, 0.1, 0.4]]
offspring = crossover(chromosomes)
print(offspring)

for i in offspring:
    print(sum(i))