import re

import nltk
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


# Function to clean text
def clean_text(text):
    text = re.sub(r'\W+', ' ', text.lower())
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text


# Function to split text into logical sentences
def split_sentences(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return sentences


# Function to remove empty sentences
def remove_empty_sentences(sentences):
    sentences = list(filter(None, sentences))
    return sentences


# Fitness function
def fitness(solution, tf_matrix):
    # Calculate the sum of the TF scores for the selected sentences
    scores = np.sum(tf_matrix * solution, axis=1)
    return np.sum(scores)


# Function to generate initial population
def generate_population(num_pop, num_sentences):
    population = np.zeros((num_pop, num_sentences))
    for i in range(num_pop):
        # Randomly select 25 sentences
        ones_indices = np.random.choice(num_sentences, size=25, replace=False)
        population[i, ones_indices] = 1
    return population


# Function to perform mutation
def mutation(solution, mutation_rate):
    for i in range(len(solution)):
        if np.random.random() < mutation_rate:
            solution[i] = 1 - solution[i]
    return solution


# Function to perform crossover
def crossover(parent1, parent2):
    child = np.zeros(len(parent1))
    crossover_point = np.random.randint(len(parent1))
    child[:crossover_point] = parent1[:crossover_point]
    child[crossover_point:] = parent2[crossover_point:]
    return child


# Function to perform selection
def selection(population, fitness_scores):
    sorted_indices = np.argsort(fitness_scores)[::-1]
    sorted_population = population[sorted_indices]
    elite = sorted_population[0]
    selected_parents = np.random.choice(sorted_population[1:], size=len(population) - 1)
    return np.concatenate((np.array([elite]), selected_parents))


# Function to run genetic algorithm
def genetic_algorithm(tf_matrix, num_pop, num_generations, mutation_rate, num_sentences):
    population = generate_population(num_pop, num_sentences)
    for i in range(num_generations):
        fitness_scores = [fitness(solution, tf_matrix) for solution in population]
        population = selection(population, fitness_scores)
        new_population = []
        for j in range(num_pop - 1):
            parent1 = population[np.random.randint(len(population))]
            parent2 = population[np.random.randint(len(population))]
            child = crossover(parent1, parent2)
            child = mutation(child, mutation_rate)
            new_population.append(child)
        population = np.concatenate((population, np.array(new_population)))
    fitness_scores = [fitness(solution, tf_matrix) for solution in population]
    best_solution = population[np.argmax(fitness_scores)]
    return best_solution


# Main function
def extract_summary(document, num_pop=100, num_generations=20, mutation_rate=0.1):
    # Clean and preprocess text
    document = clean_text(document)
    sentences = split_sentences(document)
    sentences = remove_empty_sentences(sentences)
    num_sentences = len(sentences)
    # Create TF matrix
    vectorizer = CountVectorizer()
    tf_matrix = vectorizer.fit_transform(sentences).toarray()

    # Run genetic algorithm
    solution = genetic_algorithm(tf_matrix, num_pop, num_generations, mutation_rate, num_sentences)

    # Get selected sentences
    summary = []
    for i in range(num_sentences):
        if solution[i] == 1:
            summary.append(sentences[i])

    # Join selected sentences to form the summary
    summary = ". ".join(summary)

    return summary


def main():
    # Read from file
    with open("input.txt", "r") as file:
        text = file.read()

    extract_summary(text)


if __name__ == '__main__':
    main()
