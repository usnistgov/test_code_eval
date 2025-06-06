import os
import sys

sys.path.insert(0, "../genai_code_test")
from genai_code_test.utils.create_code_files_from_json_input import func_create_code_files_from_json


def test_validate_create_code_files_from_json_input(setup_and_teardown):
    # Checking by selected paths

    config = setup_and_teardown
    config_mode = "Test"
    root_data_dir = config[config_mode]["root_data_dir"]
    root_output_dir = config[config_mode]["root_output_dir"]
    prob_data_subdir = config[config_mode]["prob_data_subdir"]
    prob_data_dir = os.path.join(root_data_dir, prob_data_subdir)
    output_subdir = config[config_mode]["script_output_subdir"]
    output_dir = os.path.join(root_output_dir, output_subdir)

    # Check 1 - json file has all the fields so should return True
    prob_json_filepath_dir = os.path.join(prob_data_dir, "testing_one")
    output_dir = os.path.join(output_dir, "testing_one_for_test_create_code_files_from_json_input")

    result = func_create_code_files_from_json(prob_json_filepath_dir, output_dir)
    assert result == True

    # Check 2 - json file has one field blank should return False
    prob_json_filepath_dir2 = os.path.join(prob_data_dir, "testing_two")
    output_dir2 = os.path.join(output_dir, "testing_two_for_test_create_code_files_from_json_input")

    result2 = func_create_code_files_from_json(prob_json_filepath_dir2, output_dir2)
    assert result2 == False

    # Check 3 - json file has more than one field blank should return False
    prob_json_filepath_dir3 = os.path.join(prob_data_dir, "testing_three")
    output_dir3 = os.path.join(output_dir, "testing_three_for_test_create_code_files_from_json_input")

    result3 = func_create_code_files_from_json(prob_json_filepath_dir3, output_dir3)
    assert result3 == False
