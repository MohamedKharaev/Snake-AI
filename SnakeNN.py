import numpy as np
import tflearn
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression

import math
import random
from statistics import mean
from collections import Counter

from Game import Board, UP, DOWN, LEFT, RIGHT, GameOver


class SnakeNN:

    def __init__(self, initial_games=10000, test_games=1000, goal_steps=2000, lr=1e-2, filename='snake_nn.tflearn'):
        self.initial_games = initial_games
        self.test_games = test_games
        self.goal_steps = goal_steps
        self.lr = lr
        self.filename = filename
        self.vectors_and_keys = [
            [[-1, 0], UP],
            [[0, 1], RIGHT],
            [[1, 0], DOWN],
            [[0, -1], LEFT]
        ]

    def generate_population(self):
        training_data = []

        for _ in range(self.initial_games):
            game = Board()
            prev_observation = self.generate_observation(game)
            #prev_food_distance = game.food_distance()
            prev_food_distance = np.linalg.norm(np.array(game.food) - np.array(game.snake[-1]))
            prev_score = game.score

            for _ in range(self.goal_steps):
                #direction = self.generate_direction(game.direction)
                action, direction = self.generate_action(game.snake)
                try:
                    game.run(direction)
                    #food_distance = game.food_distance()
                    food_distance = np.linalg.norm(np.array(game.food) - np.array(game.snake[-1]))
                    score = game.score

                    if score > prev_score or food_distance < prev_food_distance:
                        training_data.append([self.add_action_to_observation(prev_observation, action), 1])
                    else:
                        training_data.append([self.add_action_to_observation(prev_observation, action), 0])

                    prev_observation = self.generate_observation(game)
                    prev_food_distance = food_distance
                    #prev_score = score
                except GameOver as g:
                    if str(g) == "You Win":
                        training_data.append([self.add_action_to_observation(prev_observation, action), 1])
                    else:
                        training_data.append([self.add_action_to_observation(prev_observation, action), -1])
                    break

        return training_data

    def generate_action(self, snake):
        action = random.randint(0, 2) - 1
        return action, self.generate_game_action(snake, action)

    def generate_game_action(self, snake, action):
        snake_direction = self.get_snake_direction_vector(snake)
        new_direction = snake_direction
        if action == -1:
            new_direction = np.array([-snake_direction[1], snake_direction[0]])
        elif action == 1:
            new_direction = np.array([snake_direction[1], -snake_direction[0]])
        for pair in self.vectors_and_keys:
            if pair[0] == new_direction.tolist():
                game_action = pair[1]
                return game_action

    def create_model(self):
        network = input_data(shape=[None, 5, 1], name='input')
        network = fully_connected(network, 25, activation='relu')
        network = fully_connected(network, 1, activation='linear')
        network = regression(network, optimizer='adam', learning_rate=self.lr, loss='mean_square', name='target')
        model = tflearn.DNN(network, tensorboard_dir='logs')
        return model

    def train_model(self, training_data, model):
        x = np.reshape(np.array([i[0] for i in training_data]), (-1, 5, 1))
        y = np.reshape(np.array([i[1] for i in training_data]), (-1, 1))
        model.fit(x, y, n_epoch=3, shuffle=True, run_id=self.filename)
        model.save(self.filename)
        return model

    def test_model(self, model):
        steps_list = []
        scores_list = []

        for _ in range(self.test_games):
            steps = 0
            game = Board()
            prev_observation = self.generate_observation(game)

            for _ in range(self.goal_steps):
                predictions = []
                for action in range(-1, 2):
                    predictions.append(model.predict(np.reshape(self.add_action_to_observation(prev_observation, action), (-1, 5, 1))))
                action = np.argmax(np.array(predictions))
                game_action = self.generate_game_action(game.snake, action - 1)
                try:
                    game.run(game_action)
                    prev_observation = self.generate_observation(game)
                    steps += 1
                except GameOver as g:
                    print(str(g))
                    print(game.score)
                    print(steps)
                    print(prev_observation)
                    print(predictions)
                    break

            steps_list.append(steps)
            scores_list.append(game.score)

        print('Average steps:', mean(steps_list))
        print(Counter(steps_list))
        print('Average score:', mean(scores_list))
        print(Counter(scores_list))

    def generate_observation(self, game):
        snake_direction = self.get_snake_direction_vector(game.snake)
        food_direction = np.array(game.food) - np.array(game.snake[-1])
        blocked_directions = game.blocked_direction()
        angle = self.get_angle(snake_direction, food_direction)
        return np.array(blocked_directions + [angle])

    def generate_direction(self, direction):
        if direction == UP:
            directions = [UP, LEFT, RIGHT]
        elif direction == DOWN:
            directions = [DOWN, LEFT, RIGHT]
        elif direction == LEFT:
            directions = [UP, DOWN, RIGHT]
        else:
            directions = [UP, DOWN, LEFT]
        return random.choice(directions)

    def get_snake_direction_vector(self, snake):
        return np.array(list(snake[-1])) - np.array(list(snake[-2]))

    def get_angle(self, x, y):
        x = x / np.linalg.norm(x)
        y = y / np.linalg.norm(y)
        return math.atan2(x[0] * y[1] - x[1] * y[0], x[0] * y[0] + x[1] * y[1]) / math.pi

    def add_action_to_observation(self, observation, action):
        return np.append([action], observation)

    def train(self):
        training_data = self.generate_population()
        nn_model = self.create_model()
        nn_model = self.train_model(training_data, nn_model)
        self.test_model(nn_model)


if __name__ == '__main__':
    SnakeNN().train()
