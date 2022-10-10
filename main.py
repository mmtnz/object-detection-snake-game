import configuration as config_vars
from snake_game import snake_game_object_detection_mode, snake_game_keyboard_mode


def main():

    if config_vars.IS_OBJECT_DETECTION_MODE:
        snake_game_object_detection_mode(db_scores=config_vars.database, files=config_vars.FILES)
    else:
        snake_game_keyboard_mode(db_scores=config_vars.database)


if __name__ == '__main__':
    main()
