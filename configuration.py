import configparser
import sys
import os

config_file = 'configuration.ini'

try:
    config_reader = configparser.ConfigParser()
    config_reader.read(config_file)

    IS_OBJECT_DETECTION_MODE = eval(config_reader['snake']['is_object_detection_mode'])
    CUSTOM_MODEL_NAME = config_reader['snake']['custom_model_name']
    LABEL_MAP_NAME = config_reader['snake']['label_map_name']

    DB_HOST = config_reader['database']['db_host']
    DB_PASSWORD = config_reader['database']['db_password']
    DB_SCHEMA_NAME = config_reader['database']['db_schema_name']
    DB_USER = config_reader['database']['db_user']
    DB_TABLE_NAME = config_reader['database']['db_table_name']

except Exception as e:
    print(f'[!] Error reading {config_file} file -> {type(e)}: {e}')
    sys.exit()

""" Create DataBase object """
try:
    database = DataBase(
        host=DB_HOST,
        schema_name=DB_SCHEMA_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    if database.error_creating:
        print(f"[!] Error creating database object")
        database = None
    else:
        print(f'[+] Database object successfully created')
except Exception as e:
    database = None
    print(f"[!] Error creating database object -> {type(e)}: {e}")

PATHS = {
    'ANNOTATION_PATH': os.path.join('Tensorflow', 'workspace', 'annotations'),
    'MODEL_PATH': os.path.join('Tensorflow', 'workspace', 'models'),
    'CHECKPOINT_PATH': os.path.join('Tensorflow', 'workspace', 'models', CUSTOM_MODEL_NAME, 'export', 'checkpoint'),
}

FILES = {
    'PIPELINE_CONFIG': os.path.join('Tensorflow', 'workspace', 'models', CUSTOM_MODEL_NAME, 'export', 'pipeline.config'),
    'LABELMAP': os.path.join(PATHS['ANNOTATION_PATH'], LABEL_MAP_NAME)
}
