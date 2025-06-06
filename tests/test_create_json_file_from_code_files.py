import os
import sys

sys.path.insert(0, "../genai_code_test")
from genai_code_test.utils.create_json_file_from_code_files import func_create_json_file_from_code_files


def test_validate_create_json_file_from_code_files(setup_and_teardown):
    # Checking by selected paths

    config = setup_and_teardown
    config_mode = "Test"
    root_data_dir = config[config_mode]["root_data_dir"]
    root_output_dir = config[config_mode]["root_output_dir"]
    prob_data_subdir = config[config_mode]["prob_data_subdir"]
    prob_data_dir = os.path.join(root_data_dir, prob_data_subdir)
    output_subdir = config[config_mode]["script_output_subdir"]
    output_dir = os.path.join(root_output_dir, output_subdir)

    # Check 1 - folder has all the files so should return True
    prob_json_filepath_dir = os.path.join(prob_data_dir, "testing_problem_one")
    output_dir = os.path.join(output_dir, "testing_problem_one_for_test_create_code_files_from_json_input")
    # print(prob_json_filepath_dir)

    result = func_create_json_file_from_code_files(prob_json_filepath_dir, output_dir)
    print(result)
    assert result == True

    # Check 2 - folder is missing one property from the json metadata file so should return False
    prob_json_filepath_dir2 = os.path.join(prob_data_dir, "testing_problem_two")
    output_dir2 = os.path.join(output_dir, "testing_problem_two_for_test_create_code_files_from_json_input")
    # print(prob_json_filepath_dir2)

    result2 = func_create_json_file_from_code_files(prob_json_filepath_dir2, output_dir2)
    assert result2 == False

    # Check 3 - folder is missing contents from two files - metadata and correct code - so should return False
    prob_json_filepath_dir3 = os.path.join(prob_data_dir, "testing_problem_three")
    output_dir3 = os.path.join(output_dir, "testing_problem_three_for_test_create_code_files_from_json_input")
    # print(prob_json_filepath_dir3)

    result3 = func_create_json_file_from_code_files(prob_json_filepath_dir3, output_dir3)
    assert result3 == False
