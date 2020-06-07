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

    def __init__(self, initial_games = 10000, test_games = 1000, goal_steps = 2000, lr = 1e-2, filename = 'snake_nn.tflearn'):
        self.initial_games = initial_games
        self.test_games = test_games
        self.goal_steps = goal_steps
        self.lr = lr
        self.filename = filename
        self.directions_and_moves = {repr([-1, 0]): UP, 
                                     repr([0, 1]): RIGHT, 
                                     repr([1, 0]): DOWN, 
                                     repr([0, -1]): LEFT}

    def generate_population(self):
        training_data = []

        for init_game in range(self.initial_games):
            game = Board()
            prev_observation = self.generate_observation(game)
            prev_food_distance = np.linalg.norm(np.array(game.food) - np.array(game.snake[-1]))
            prev_score = game.score

            for step in range(self.goal_steps):
                action, direction = self.generate_action(game.snake)
                try:
                    game.run(direction)
                    food_distance = np.linalg.norm(np.array(game.food) - np.array(game.snake[-1]))
                    score = game.score

                    if score > prev_score or food_distance < prev_food_distance:
                        training_data.append([self.add_act_to_observ(prev_observation, action), 1])
                    else:
                        training_data.append([self.add_act_to_observ(prev_observation, action), 0])

                    prev_observation = self.generate_observation(game)
                    prev_food_distance = food_distance
                except GameOver as g:
                    if str(g) == "You Win":
                        training_data.append([self.add_act_to_observ(prev_observation, action), 1])
                    else:
                        training_data.append([self.add_act_to_observ(prev_observation, action), -1])
                    break

        return training_data

    def generate_action(self, snake):
        action = random.randint(-1, 1)
        return action, self.generate_game_move(snake, action)

    def generate_game_move(self, snake, action):
        snake_direction = self.calc_snake_direction_vector(snake)
        modified_dir = snake_direction
        if action == -1:
            modified_dir = np.array([-snake_direction[1], snake_direction[0]])
        elif action == 1:
            modified_dir = np.array([snake_direction[1], -snake_direction[0]])

        return self.directions_and_moves[str(modified_dir.tolist())]

    def create_nn_model(self):
        network = input_data(shape = [None, 5, 1], name = 'input')
        network = fully_connected(network, 25, activation = 'relu')
        network = fully_connected(network, 1, activation = 'linear')
        network = regression(network, optimizer = 'adam', learning_rate = self.lr, loss = 'mean_square', name = 'target')
        model = tflearn.DNN(network, tensorboard_dir = 'logs')
        return model

    def train_nn_model(self, training_data, model):
        x_tr = []
        y_tr = []

        for tr in training_data:
            x_tr.append(tr[0])
            y_tr.append(tr[1])

        x_tr = np.array(x_tr).reshape(-1, 5, 1)
        y_tr = np.array(y_tr).reshape(-1, 1)

        model.fit(x_tr, y_tr, n_epoch = 3, shuffle = True, run_id = self.filename)
        model.save(self.filename)
        return model

    def test_model(self, model):
        steps_list = []
        scores_list = []

        for test_game in range(self.test_games):
            steps = 0
            game = Board()
            prev_observation = self.generate_observation(game)

            for goal_step in range(self.goal_steps):
                predictions = []
                for action in [-1, 0, 1]:
                    predictions.append(model.predict(np.reshape(self.add_act_to_observ(prev_observation, action), (-1, 5, 1))))
                action = np.argmax(np.array(predictions)) - 1
                game_move = self.generate_game_move(game.snake, action)
                try:
                    game.run(game_move)
                    prev_observation = self.generate_observation(game)
                    steps += 1
                except GameOver as g:
                    print("Test game %d had score %d and took %d steps" % (test_game, game.score, steps))
                    break

            steps_list.append(steps)
            scores_list.append(game.score)

        print('Average steps: ', mean(steps_list))
        print(Counter(steps_list))

        print('Average score: ', mean(scores_list))
        print(Counter(scores_list))

    def generate_observation(self, game):
        snake_direction = self.calc_snake_direction_vector(game.snake)
        food_direction = np.array(game.food) - np.array(game.snake[-1])
        blocked_directions = game.blocked_direction()
        angle = self.get_snake_and_food_angle(snake_direction, food_direction)
        return np.array(blocked_directions + [angle])

    def calc_snake_direction_vector(self, snake):
        return np.array(list(snake[-1])) - np.array(list(snake[-2]))

    def get_snake_and_food_angle(self, x, y):
        x = x / np.linalg.norm(x)

        y = y / np.linalg.norm(y)

        return math.atan2(x[0] * y[1] - x[1] * y[0], x[0] * y[0] + x[1] * y[1]) / math.pi

    def add_act_to_observ(self, observation, action):
        return np.append([action], observation)

    def train(self):
        training_data = self.generate_population()
        nn_model = self.create_nn_model()
        nn_model = self.train_nn_model(training_data, nn_model)
        self.test_model(nn_model)


if __name__ == '__main__':
    SnakeNN().train()