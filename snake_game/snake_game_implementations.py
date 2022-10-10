import keyboard
import cv2
from snake_game.snake_game_class import Snake
import numpy as np
import os
import tensorflow as tf
import object_detection
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import configuration as config_vars


def snake_game_keyboard_mode(db_scores=None):
    """
    Snake game a-s-d-w keys mode:
    a: go left
    s: go down
    d: go right
    w: go up

    esc: close game
    space: restart game
    """

    snake = Snake(db_scores=db_scores)
    direction = ''

    while True:

        if keyboard.is_pressed('w'):
            direction = 'up'
        elif keyboard.is_pressed('s'):
            direction = 'down'
        elif keyboard.is_pressed('a'):
            direction = 'left'
        elif keyboard.is_pressed('d'):
            direction = 'right'
        elif keyboard.is_pressed(' '):
            snake.reset_game()
        elif keyboard.is_pressed('\x1b'):
            cv2.destroyAllWindows()
            break

        if direction == 'up':
            snake.move_up()
        elif direction == 'down':
            snake.move_down()
        elif direction == 'left':
            snake.move_left()
        elif direction == 'right':
            snake.move_right()
        snake.plot_snake()


# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(config_vars.FILES['PIPELINE_CONFIG'])
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(config_vars.PATHS['CHECKPOINT_PATH'], 'ckpt-0')).expect_partial()


@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections


def snake_game_object_detection_mode(db_scores=None, files=None):
    """
    Snake game played with hand gestures thanks to object detecion
    :param db_scores: database to store scores
    :param files: dictionary with files paths
    :return:
    """

    category_index = label_map_util.create_category_index_from_labelmap(files['LABELMAP'])

    cap = cv2.VideoCapture(0)
    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = 600
    height = 800

    snake = Snake(db_scores=db_scores)

    while cap.isOpened():
        ret, frame = cap.read()
        image_np = np.array(frame)

        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
        detections = detect_fn(input_tensor)

        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                      for key, value in detections.items()}
        detections['num_detections'] = num_detections

        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        label_id_offset = 1
        image_np_with_detections = image_np.copy()

        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes'] + label_id_offset,
            detections['detection_scores'],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=5,
            min_score_thresh=.6,
            agnostic_mode=False)

        cv2.imshow('object detection', cv2.resize(image_np_with_detections, (height, width)))
        snake.plot_snake()

        for i in range(len(detections['detection_scores'])):
            if detections['detection_scores'][i] > 0.6:
                class_id = detections['detection_classes'][i] + 1
                if class_id == 1:
                    snake.move_up()
                elif class_id == 2:
                    snake.move_down()
                elif class_id == 3:
                    snake.move_left()
                elif class_id == 4:
                    snake.move_right()
                snake.plot_snake()

        if keyboard.is_pressed('\x1b'):
            cv2.destroyAllWindows()
            break

        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
