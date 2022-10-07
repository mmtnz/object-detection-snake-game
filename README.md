# object-detection-snake-game
Snake game which is controlled by hand gestures thanks to object detection API

### Table of Contents
<details>
  <summary>Click me</summary>
  
  ### Contents
  1. [Description](#description)
  2. [Built With](#built-with)
  3. [Challenges](#challenges)
  4. [Getting Started](#getting-started)
</details>

## Description

This repository has been created with the aim of understanding how the object detection API works.

With the object detecion API and a pretrained model it is possible to capture hand's position which are used to change snake's direction. The model has been trained following the ############ object detection tutorial. It could be retrained if it is not working properly.

The snake game is defined as a class with different methods to move the snake. Probably there are better python implementations of this game due to its age. However, the game is only used as a demo and I wanted to face the game implementation on my own.

A keyboard mdoe implementation is also included.

### Built With

- [![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/) | [![iPython 8.5](https://img.shields.io/badge/ipython-8.5-yellow.svg)](https://www.python.org/downloads/release/python-390/): Both python and ipython versions are implemented and included.
- [![TensorFlow 2](https://img.shields.io/badge/TensorFlow_Object_Detection_API-2.2-FF6F00?logo=tensorflow)](https://github.com/tensorflow/models/blob/master/research/object_detection): TensorFlow Object Detecion API to detect the different hand positions
- [![mysql](https://img.shields.io/badge/MySQL-database-green?style=flate&logo=mysql&logoColor=white.svg)](https://mysql.com/) : MySql database is (optionally) used to gather scores. This allows to share scores between different players.

## Getting started

In this section it will be shown how to run the app locally.

The first step is to clone this repository in a local folder.

### Prerequisites

- #### Requirements:
Create and activate a new virtual enviroment.
```sh
python3 -m venv project_local_folder/myvenv
cd project_local_folder/myvenv/scripts
activate
```

Install the requirements.
```sh
cd project_local_folder
pip install -r requirements.txt
```

- #### Train model (optional)
This repository includes an already trained model. However, sometimes could be interesting to train it again if it is not working properly.

- #### Launch program

For 


`Indicar pasos a seguir`

## Acknowledgment

I want to thanks USUARIO for his `Object Detection` tutorial

