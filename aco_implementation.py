import numpy as np
import matplotlib.pyplot as plt
import random

class AntColonyOptimization:
    def __init__(self, points, n_ants=10, n_iterations=100, alpha=1, beta=1, evaporation_rate=0.5, q_val=1):
        """
        :param points: nodes to be connected
        :param n_ants: agents to be used
        :param n_iterations: iterations to be run
        :param alpha: exponent on pheromone
        :param beta: exponent on distance
        :param evaporation_rate: Decay rate of pheromone
        :param q_val: pheromone to be deposited
        """
        self.points = points
        self.n_points = len(points)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.q_val = q_val
        self.pheromone = np.ones((self.n_points, self.n_points))
        self.best_path = None
        self.best_path_length = np.inf

    def distance(self, point1, point2):
        """
        Calculates the distance between two points
        :return: float of distance
        """
        # Uses Euclidean distance to calculate distance between two points
        return np.sqrt(np.sum((point1 - point2) ** 2))

    def run(self):
        """
        Runs the algorithm using functions defined below
        :return: best path and its length
        """
        for iteration in range(self.n_iterations):
            paths = []
            path_lengths = []
            self.generate_paths(paths, path_lengths)
            self.update_pheromone_trail(paths, path_lengths)
        self.plot()
        return self.best_path, self.best_path_length

    def update_pheromone_trail(self, paths, path_lengths):
        """
        Updates the pheromone trail
        :param paths: all paths taken
        :param path_lengths: lengths of all paths
        :return: None
        """
        # Evaporates pheromone with evaporation rate
        self.pheromone *= self.evaporation_rate

        # Adds pheromone to paths taken
        for path, path_length in zip(paths, path_lengths):
            for i in range(self.n_points - 1):
                # Adds pheromone to path
                self.pheromone[path[i], path[i + 1]] += self.q_val / path_length
            # Adds pheromone to reverse path
            self.pheromone[path[-1], path[0]] += self.q_val / path_length

    def generate_path(self, visited, path, path_length, current_point):
        """
        Generates a path for an ant
        :param visited: array of visited points
        :param path: path taken
        :param path_length: length of path taken
        :return: path taken and length of path taken
        """
        # Generates a path until all points are visited
        while False in visited:
            # Creates an array of unvisited points and an array of probabilities
            unvisited = [i for i in range(len(visited)) if not visited[i]]
            probabilities = [0] * len(unvisited)

            # Calculates the probability of each unvisited point
            for i, unvisited_point in enumerate(unvisited):
                probabilities[i] = self.pheromone[current_point, unvisited_point] ** self.alpha / self.distance(
                    self.points[current_point], self.points[unvisited_point]) ** self.beta

            # Normalizes the probabilities
            probabilities /= np.sum(probabilities)

            # Chooses the next point based on the probabilities
            next_point = np.random.choice(unvisited, p=probabilities)
            path.append(next_point)
            # Adds the distance between the current point and the next point to the path length
            path_length += self.distance(self.points[current_point], self.points[next_point])
            # Sets the next point as visited and sets the next point as the current point
            visited[next_point] = True
            current_point = next_point

        return path, path_length

    def generate_paths(self, paths, path_lengths):
        """
        Generates paths for each ant and appends it to paths and path_lengths
        :param paths: all paths taken
        :param path_lengths: lengths of all paths
        :return: None
        """
        # Generates paths for each ant
        for ant in range(self.n_ants):
            # Initializes an array of visited points
            visited = [False] * self.n_points
            # Chooses a random starting point
            current_point = random.randrange(self.n_points)
            # Sets the starting point as visited
            visited[current_point] = True
            # Initializes the path and path length
            path = [current_point]
            path_length = 0
            path, path_length = self.generate_path(visited, path, path_length, current_point)
            paths.append(path)
            path_lengths.append(path_length)

            # Updates the best path and best path length if the path length is shorter
            if path_length < self.best_path_length:
                self.best_path = path
                self.best_path_length = path_length

    def plot(self):
        """
        Plots the points and the best path
        :return: None
        """
        # Plots the points of the unconnected points
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
        ax[0].scatter(self.points[:, 0], self.points[:, 1], c='r', marker='o')
        ax[0].set_xlabel('X Label')
        ax[0].set_ylabel('Y Label')
        ax[0].set_title('Unconnected Points')

        # Plots the best path
        ax[1].scatter(self.points[:, 0], self.points[:, 1], c='r', marker='o')
        for i in range(self.n_points - 1):
            ax[1].plot([self.points[self.best_path[i], 0], self.points[self.best_path[i + 1], 0]],
                       [self.points[self.best_path[i], 1], self.points[self.best_path[i + 1], 1]],
                       c='g', linestyle='-', linewidth=2, marker='o')
        ax[1].plot([self.points[self.best_path[0], 0], self.points[self.best_path[-1], 0]],
                   [self.points[self.best_path[0], 1], self.points[self.best_path[-1], 1]],
                   c='g', linestyle='-', linewidth=2, marker='o')
        ax[1].set_xlabel('X Label')
        ax[1].set_ylabel('Y Label')
        ax[1].set_title(f'Shortest Path ({self.best_path_length:.2f})')

        # Shows the plot
        plt.show()


def read_data(file_name: str):
    """
    Reads data from file
    :param file_name: string of file name
    :return: 2D list of data
    """
    # Reads data from file
    data = []
    # Checks if file exists
    try:
        file = open(file_name, 'r')
    except FileNotFoundError:
        # If file does not exist, asks user to try again
        print("File not found! Please try again!")
        return read_data(input('Enter file name: '))

    # Reads data from file line by line
    for line in file:
        x, y = line.strip().split(',')
        # Appends data to list
        data.append([float(x), float(y)])
    # Closes file
    file.close()
    # Returns data as numpy array
    return np.array(data)


def main():
    # Asks user for file name
    print("Welcome to the Ant Colony Optimization program!")
    file_name = input("Enter file name of the coordinates: ")
    points = read_data(file_name)
    # Asks user for parameters
    ants = int(input("Enter number of ants: "))
    iterations = int(input("Enter number of iterations: "))
    decay = float(input("Enter evaporation rate: "))
    alpha, beta = 1, 1
    # Checks if number of ants is greater than number of points
    if ants > len(points) or iterations > len(points):
        # If so, asks user to wait as runtime will be long
        print("Please wait while the program runs...")

    # Runs the algorithm
    aco = AntColonyOptimization(points, ants, iterations, alpha, beta, decay, q_val=1)
    aco.run()

    # Prints thank you message
    print("Thank you for using this program!")


if __name__ == '__main__':
    main()
