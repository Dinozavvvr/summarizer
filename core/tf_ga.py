import re
import random

import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize


# Method for minimal clearing of the text
def clean_text(text):
    # Split text into sentences
    sentences = sent_tokenize(text)

    # Remove numbers, punctuation except dots, and stop words
    stop_words = set(stopwords.words('english'))
    clean_sentences = []
    for sentence in sentences:
        sentence = sentence.lower()
        sentence = re.sub(r'\d+', '', sentence)
        sentence = re.sub(r'[^\w\s]', '', sentence)
        words = sentence.split()
        words = [word for word in words if word not in stop_words]
        sentence = ' '.join(words)
        sentence = re.sub(r'\s+', ' ', sentence).strip()
        if sentence:
            clean_sentences.append(sentence)

    return clean_sentences


# Initializing population
def initialize_population(num_pop, num_sentences):
    return np.random.randint(2, size=(num_pop, num_sentences))


# Fitness
def fitness(solution, tf_matrix):
    # Reshape solution to have shape (362,1)
    solution = solution.reshape((-1, 1))

    # Calculate the sum of the TF scores for the selected sentences
    scores = np.sum(tf_matrix * solution, axis=1)
    return np.sum(scores)


# Mutation
def mutate(solution):
    # Determine the number of zeros in the current solution
    num_zeros = len(solution) - np.count_nonzero(solution)

    # Randomly select up to num_zeros bits to toggle
    indices = np.random.choice(np.where(solution == 0)[0], size=min(num_zeros, 25), replace=False)
    new_solution = solution.copy()
    new_solution[indices] = 1 - new_solution[indices]

    return new_solution


# Crossover function
def crossover(parent1, parent2):
    # Choose a random crossover point
    crossover_point = random.randint(1, len(parent1) - 1)

    # Perform the crossover
    child1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
    child2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))

    return child1, child2


# Parent selecting
def select_parents(population, fitness_scores):
    # Select two parents using tournament selection
    indices = np.random.choice(len(population), size=2, replace=False)
    parents = population[indices]
    parent_fitness_scores = fitness_scores[indices]
    return parents[np.argmax(parent_fitness_scores)]


# Define the genetic algorithm function
# def genetic_algorithm(tf_matrix, pop_size=50, n_gen=100, p_cross=0.9, p_mut=0.1):
#     # Initialize the population
#     pop = np.random.randint(0, 2, size=(pop_size, tf_matrix.shape[0]))
#     # Iterate over generations
#     for gen in range(n_gen):
#         # Evaluate fitness
#         fitness_values = np.array([fitness(solution, tf_matrix) for solution in pop])
#         # Select the most fit individuals
#         tournament_idx = np.random.choice(pop_size, size=(pop_size, 2))
#         winners = np.array([pop[idx[np.argmax(fitness_values[idx])]] for idx in tournament_idx])
#         # Perform crossover
#         for i in range(pop_size // 2):
#             if np.random.rand() < p_cross:
#                 # Select two parents
#                 parent1, parent2 = winners[i * 2], winners[i * 2 + 1]
#                 # Perform crossover
#                 crossover_point = np.random.randint(0, tf_matrix.shape[0])
#                 offspring1 = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
#                 offspring2 = np.concatenate([parent2[:crossover_point], parent1[crossover_point:]])
#                 # Replace parents with offspring
#                 winners[i * 2], winners[i * 2 + 1] = offspring1, offspring2
#         # Perform mutation
#         for i in range(pop_size):
#             if np.random.rand() < p_mut:
#                 # Select a random bit to flip
#                 mutation_point = np.random.randint(0, tf_matrix.shape[0])
#                 winners[i, mutation_point] = 1 - winners[i, mutation_point]
#         # Replace least fit individuals with new offspring
#         fitness_values = np.array([fitness(solution, tf_matrix) for solution in winners])
#         sorted_idx = np.argsort(-fitness_values)
#         pop = winners[sorted_idx]
#     # Return the best solution
#     return pop[0]


def genetic_algorithm(tf_matrix, num_pop, num_generations):
    # Initialize the population
    population = initialize_population(num_pop, tf_matrix.shape[0])

    # Evaluate the fitness of the initial population
    fitness_scores = np.array([fitness(solution, tf_matrix) for solution in population])

    # Keep track of the best solution and its fitness
    best_solution = population[np.argmax(fitness_scores)]
    best_fitness = fitness_scores[np.argmax(fitness_scores)]

    # Run the genetic algorithm for num_generations generations
    for i in range(num_generations):
        # Select parents for crossover
        parent1 = select_parents(population, fitness_scores)
        parent2 = select_parents(population, fitness_scores)

        # Perform crossover to produce two children
        child1, child2 = crossover(parent1, parent2)

        # Mutate the children
        child1 = mutate(child1)
        child2 = mutate(child2)

        # Evaluate the fitness of the children
        child1_fitness = fitness(child1, tf_matrix)
        child2_fitness = fitness(child2, tf_matrix)

        # Replace the two worst solutions in the population with the children
        worst_indices = np.argsort(fitness_scores)[:2]
        population[worst_indices[0]] = child1
        population[worst_indices[1]] = child2

        # Update the fitness scores
        fitness_scores[worst_indices[0]] = child1_fitness
        fitness_scores[worst_indices[1]] = child2_fitness

        # Update the best solution if necessary
        if child1_fitness > best_fitness:
            best_solution = child1
            best_fitness = child1_fitness

        if child2_fitness > best_fitness:
            best_solution = child2
            best_fitness = child2_fitness

    # Return the best solution
    return best_solution


def main():
    # Read from file
    with open("input.txt", "r") as file:
        text = file.read()

    # Clear the text and split to sentence
    sentences = clean_text(text)

    # Preprocess the input data
    vectorizer = TfidfVectorizer(stop_words='english')
    tf_matrix = vectorizer.fit_transform(sentences).toarray()

    # Run the genetic algorithm
    num_pop = 100
    num_generations = 100
    solution = genetic_algorithm(tf_matrix, num_pop, num_generations)

    # Print the selected sentences
    selected_indices = np.where(solution == 1)[0]
    selected_sentences = [sentences[i] for i in selected_indices]
    selected_sentences = sorted(selected_sentences, key=lambda s: np.sum(tf_matrix[sentences.index(s)]))
    selected_sentences = selected_sentences[::-1][:25]

    print('\n'.join(selected_sentences))


if __name__ == '__main__':
    main()

# # Call the genetic_algorithm function
# best_solution = genetic_algorithm(tf_matrix)
# important_sentences = [sentences[i] for i, val in enumerate(best_solution) if val == 1]
# print(important_sentences)
#
# sentences = clean_text(text)
