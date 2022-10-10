import random
import keyboard
import cv2
import numpy as np


class Snake:

    def __init__(self, screen_width: int = 500, screen_height: int = 500, pixel_size: int = 20,
                 db_scores=None):

        # Params
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._pixel_size = pixel_size  # how many actual pixels fill every game pixel
        self._num_width_pixels = int(self._screen_width / self._pixel_size)
        self._num_height_pixels = int(self._screen_height / self._pixel_size)

        # db
        self._db_scores = db_scores

        # Positions -> Snake starts at the middle of the screen
        self._snake_head_pos = [int(self._num_height_pixels / 2), int(self._num_height_pixels / 2)]
        self._snake_body_pos_list = []
        self._snake_body_direction_list = []
        self._apple_position = None
        self._update_apple_position()  # Initialize apple position
        self._last_direction = None

        # Colors
        self._background_color = (232, 124, 29)
        self._snake_head_color = (0, 255, 0)
        self._snake_body_color = (54, 151, 18)
        self._apple_color = (112, 80, 255)

        # Screen
        self._screen = np.full((self._screen_height, self._screen_width, 3), self._background_color, dtype=np.uint8)
        self._score = 0
        self._local_scores_list = []  # To store scores if there is not db
        self._db_scores_list = None
        self._is_player_name = False
        self._player_name = ''
        self._ordinal_list = ['st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th']

        # Booleans
        self._body_needs_update = True
        self._there_was_apple = False
        self._is_game_over = False

        # Text params
        self._score_text = 'Score: {}'  # score will be placed between {}
        self._score_text_options = {'org': (self._screen_width - 150, 35), 'fontFace': cv2.FONT_HERSHEY_SIMPLEX,
                                    'fontScale': 1, 'color': (255, 255, 255), 'thickness': 2, 'lineType': cv2.LINE_AA}
        self._game_over_text_options = {'text': 'Game Over', 'org': (int(self._screen_width / 2) - 130, 100),
                                        'fontFace': cv2.FONT_HERSHEY_SIMPLEX, 'fontScale': 1.5, 'color': (0, 0, 255),
                                        'thickness': 2, 'lineType': cv2.LINE_AA}
        self._final_score_text_options = {'org': (int(self._screen_width / 2) - 73, 200),
                                          'fontFace': cv2.FONT_HERSHEY_SIMPLEX,
                                          'fontScale': 1, 'color': (0, 0, 0), 'thickness': 2, 'lineType': cv2.LINE_AA}
        self._player_name_text_options = {'org': (int(self._screen_width / 2) - 125, 300),
                                          'fontFace': cv2.FONT_HERSHEY_SIMPLEX, 'fontScale': 1, 'color': (51, 207, 245),
                                          'thickness': 2, 'lineType': cv2.LINE_AA}
        self._score_list_text_options = {'fontFace': cv2.FONT_HERSHEY_SIMPLEX, 'fontScale': 0.8,
                                         'thickness': 2, 'lineType': cv2.LINE_AA}

        self._score_list_pos = (
            self._game_over_text_options['org'][0] + 50, self._game_over_text_options['org'][1] + 60)
        self._score_list_text_color = (0, 0, 255)
        self._score_list_new_text_color = (0, 255, 255)  # If new score is top 6, other color

    """ Player methods """

    # Coordinates (0,0) are top let
    def move_up(self):
        """ To move snake position one step up """
        self._snake_head_pos[0] = (self._snake_head_pos[0] - 1) % self._num_height_pixels
        self._last_direction = 'up'
        self._move_snake()

    def move_down(self):
        """ To move snake position one step down """
        self._snake_head_pos[0] = (self._snake_head_pos[0] + 1) % self._num_height_pixels
        self._last_direction = 'down'
        self._move_snake()

    def move_left(self):
        """ To move snake position one step left """
        self._snake_head_pos[1] = (self._snake_head_pos[1] - 1) % self._num_width_pixels
        self._last_direction = 'left'
        self._move_snake()

    def move_right(self):
        """ To move snake position one step right """
        self._snake_head_pos[1] = (self._snake_head_pos[1] + 1) % self._num_width_pixels
        self._last_direction = 'right'
        self._move_snake()

    def plot_snake(self):
        """ To generate the screen """
        if not self._is_game_over:
            self._update_screen()
        else:
            if not self._is_player_name:
                self._get_name_screen()  # Screen to write player name
            else:
                self._game_over_screen()  # To show top 10 scores

    def reset_game(self):
        """ To reset the game"""
        self._score = 0
        self._snake_head_pos = [int(self._num_height_pixels / 2), int(self._num_height_pixels / 2)]
        self._snake_body_pos_list = []
        self._snake_body_direction_list = []
        self._update_apple_position()  # Initialize apple position

        self._is_player_name = False
        self._player_name = ''
        self._body_needs_update = True
        self._there_was_apple = False
        self._is_game_over = False

    """ Class methods """

    def _move_snake(self):
        """ To move snake position """
        # To check if head new position is over an apple
        self._check_if_apple()

        # To update body position
        # It won't be done next iteation after eating an apple (only head is moving to increase size)
        if self._body_needs_update:
            self._update_body_positions()
        else:
            self._snake_body_direction_list.insert(0, self._last_direction)
            self._body_needs_update = True

        # If there was an apple, size is increased and it is indicated that next iteration body won't move
        if self._there_was_apple:
            self._increase_snake_size()
            self._body_needs_update = False
            self._there_was_apple = False  # To reset bool
        else:
            self._check_is_dead()

    def _update_body_positions(self):
        """ To move each body's pixel in its direction """
        next_direction = self._last_direction
        index = 0
        for body_position in self._snake_body_pos_list:
            direction = self._snake_body_direction_list[index]

            if direction == 'up':
                body_position[0] = (body_position[0] - 1) % self._num_height_pixels
            elif direction == 'down':
                body_position[0] = (body_position[0] + 1) % self._num_height_pixels
            elif direction == 'left':
                body_position[1] = (body_position[1] - 1) % self._num_width_pixels
            elif direction == 'right':
                body_position[1] = (body_position[1] + 1) % self._num_width_pixels

            self._snake_body_direction_list[index] = next_direction
            next_direction = direction
            index += 1

    def _check_is_dead(self):
        """ To check if head's new position will be over body """
        if self._snake_head_pos in self._snake_body_pos_list:
            self._is_game_over = True

    def _check_if_apple(self):
        """ If there is an apple in new position: score+1, new apple is created """
        if self._snake_head_pos == self._apple_position:
            self._score += 1
            self._update_apple_position()
            self._there_was_apple = True

    def _update_apple_position(self):
        """ New position created randomly, new head position will be avoided """
        x = random.randint(0, self._num_width_pixels - 1)
        y = random.randint(0, self._num_height_pixels - 1)
        self._apple_position = [y, x]
        if self._snake_head_pos == self._apple_position:
            self._update_apple_position()  # iteratively until they are not the same position

    def _increase_snake_size(self):
        """ Current head position is added to the body """
        y = self._snake_head_pos[0]  # If the atribute is asigned directly , value will change
        x = self._snake_head_pos[1]

        # It is inserted into the beginning (to be read in order)
        self._snake_body_pos_list.insert(0, [y, x])  # , self._last_direction])

    def _update_screen(self):
        """ To fill screen """
        # Background
        self._screen[:, :, :] = self._background_color

        # Snake body
        for pixel_pos in self._snake_body_pos_list:
            self._pixel_coloring(pixel_pos=pixel_pos, pixel_color=self._snake_body_color)

        # Snake head
        self._pixel_coloring(pixel_pos=self._snake_head_pos, pixel_color=self._snake_head_color)

        # Apple
        self._pixel_coloring(pixel_pos=self._apple_position, pixel_color=self._apple_color)

        # Score
        self._add_text_score()

        cv2.imshow('Snake Game', self._screen)
        cv2.waitKey(75)

    def _pixel_coloring(self, pixel_pos, pixel_color):
        """ To paint the pixel position with the selected color """
        self._screen[pixel_pos[0] * self._pixel_size: (pixel_pos[0] * self._pixel_size) + self._pixel_size,
        pixel_pos[1] * self._pixel_size: (pixel_pos[1] * self._pixel_size) + self._pixel_size, :] = pixel_color

    def _add_text_score(self):
        """" To add text with score """
        cv2.putText(self._screen, text=self._score_text.format(self._score), **self._score_text_options)

    def _game_over_screen(self):
        """" To add game over text"""
        self._screen[:, :, :] = self._background_color
        cv2.putText(self._screen, **self._game_over_text_options)
        scores_origin = self._score_list_pos
        i = 1
        scores_list = self._get_scores()

        for score in scores_list:
            if score != (self._player_name, self._score):
                color = self._score_list_text_color
            else:
                color = self._score_list_new_text_color  # Current score is showed in other color
            cv2.putText(self._screen, text=f'{i}{self._ordinal_list[i - 1]} {score[0]}: {score[1]}', org=scores_origin,
                        color=color,
                        **self._score_list_text_options)
            scores_origin = (self._score_list_pos[0], self._score_list_pos[1] + i * 40)
            i += 1
        cv2.imshow('Snake Game', self._screen)
        cv2.waitKey(75)

    def _update_scores_list(self):
        """ Update top 10 scores list (in db or local)"""
        if self._db_scores is not None:
            self._db_scores.insert_query(table_name='scores', values=(self._player_name, self._score))
        else:
            self._local_scores_list.append((self._player_name, self._score))
            sorted_by_score = sorted(self._local_scores_list, key=lambda tup: tup[1])
            self._local_scores_list = sorted_by_score[-10:]  # 6 highest scores
            self._local_scores_list.reverse()

    def _get_scores(self):
        """ To get scores locally or from database"""
        scores = []
        if self._db_scores is not None:
            scores = self._db_scores.select_query(table_name='scores', order_by_column='score', order_asc=False)
            item_to_remove = scores[11]
            if item_to_remove:
                self._db_scores.delete_query(table_name='scores',
                                             condition=f"name = {item_to_remove[0]} AND score = {item_to_remove[1]}")
                scores = scores[:-1]
        else:
            scores = self._local_scores_list
        return scores

    def _get_name_screen(self):
        """ Screen to get player name"""
        self._screen[:, :, :] = self._background_color
        cv2.putText(self._screen, **self._game_over_text_options)
        cv2.putText(self._screen, text=self._score_text.format(self._score), **self._final_score_text_options)
        cv2.putText(self._screen, text=f'Name: {self._player_name}', **self._player_name_text_options)

        cv2.imshow('Snake Game', self._screen)
        letter = cv2.waitKey(0)
        if letter == ord('\r'):
            self._is_player_name = True
            self._update_scores_list()
        elif letter == 8:  # Delete last letter
            self._player_name = self._player_name[:-1]
        else:
            try:
                if len(self._player_name) < 8:
                    self._player_name += chr(letter)
            except Exception as e:
                print(f'Char not supported -> {type(e)}: {e}')
