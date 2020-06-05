import numpy as np
import tflearn
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression

import math

from Game import Board


class SnakeNN:

    def __init__(self, initial_games=10000, test_games=1000, goal_steps=2000, lr=1e-2, filename='snake_nn.tflearn'):
        self.initial_games = initial_games
        self.test_games = test_games
        self.goal_steps = goal_steps
        self.lr = lr
        self.filename = filename
        self.vector_dict = {
            [-1, 0]: 0,
            [0, 1]: 1,
            [1, 0]: 2,
            [0, -1]: 3
        }

    def generate_population(self):
        training_data = []

        for _ in range(self.initial_games):
            game = Board()
            prev_observation = self.generate_observation(game)
            prev_food_distance = game.food_distance()

            for _ in range(self.goal_steps):
                pass

        return training_data

    def create_model(self):
        network = input_data(shape=[None, 5, 1], name='input')
        network = fully_connected(network, 25, activation='relu')
        network = fully_connected(network, 1, activation='linear')
        network = regression(network, optimizer='adam', learning_rate=self.lr, loss='mean_square', name='targets')
        model = tflearn.DNN(network, tensorboard_dir='tflearn_logs')
        return model

    def generate_observation(self, game):
        snake_direction = self.get_snake_direction_vector(game.snake)
        food_direction = np.array(game.food) - np.array(game.snake)
        blocked_directions = game.blocked_direction()
        angle = self.get_angle(snake_direction, food_direction)
        return np.array(blocked_directions + [angle])

    def get_snake_direction_vector(self, snake):
        if len(snake) > 1:
            return np.array(list(snake[0])) - np.array(list(snake[1]))
        return np.array([0, 0])

    def get_angle(self, x, y):
        x = x / np.linalg.norm(x)
        y = y / np.linalg.norm(y)
        return math.atan2(x[0] * y[1] - x[1] * y[0], x[0] * y[0] + x[1] * y[1]) / math.pi
