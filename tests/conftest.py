import pytest
import sys
import configparser
import os
import shutil


def read_config_file():
    print("Reading Config File")
    config_filepath = os.environ["GENAI_CODE_CONFIG_PATH"]

    try:
        config = configparser.ConfigParser()
        with open(config_filepath) as configfile:
            config.read_file(configfile)
    except ImportError:
        sys.exit("Cannot open config file: " + config_filepath)
    return config


@pytest.fixture(scope="session")
def setup_and_teardown():
    print("Setting Up Testing Environment in setup_and_teardown()")
    # if keep_output_after is True, delete output on setup
    # if keep_output_after is False, delete output on teardown
    keep_output_after = True
    config = read_config_file()
    config_mode = "Test"
    root_output_dir = config[config_mode]["root_output_dir"]
    sc_output_subdir = config[config_mode]["script_output_subdir"]
    val_output_subdir = config[config_mode]["validate_output_subdir"]
    eval_output_subdir = config[config_mode]["eval_output_subdir"]
    sc_output_dir = os.path.join(root_output_dir, sc_output_subdir)
    val_output_dir = os.path.join(root_output_dir, val_output_subdir)
    eval_output_dir = os.path.join(root_output_dir, eval_output_subdir)
    if not os.path.isdir(sc_output_dir):
        os.makedirs(sc_output_dir)
    if not os.path.isdir(val_output_dir):
        os.makedirs(val_output_dir)
    if not os.path.isdir(eval_output_dir):
        os.makedirs(eval_output_dir)

    if keep_output_after:
        print("Deleting Test Output for Fresh Start")
        shutil.rmtree(sc_output_dir)
        shutil.rmtree(eval_output_dir)
        shutil.rmtree(val_output_dir)

    if not os.path.isdir(sc_output_dir):
        os.makedirs(sc_output_dir)
    if not os.path.isdir(val_output_dir):
        os.makedirs(val_output_dir)
    if not os.path.isdir(eval_output_dir):
        os.makedirs(eval_output_dir)

    # Return the Config File
    yield config

    print("Tearing Down Testing Environment in setup_and_teardown()")
    if not keep_output_after:
        print("Deleting Test Output for Clean Exit")
        shutil.rmtree(sc_output_dir)
        shutil.rmtree(eval_output_dir)
        shutil.rmtree(val_output_dir)
        if not os.path.isdir(sc_output_dir):
            os.makedirs(sc_output_dir)
        if not os.path.isdir(val_output_dir):
            os.makedirs(val_output_dir)
        if not os.path.isdir(eval_output_dir):
            os.makedirs(eval_output_dir)
