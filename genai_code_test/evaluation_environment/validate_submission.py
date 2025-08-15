#! /usr/bin/env python
# Code to run submission test on correct version of front_times_input

import os
import configparser
import shutil
import sys
import argparse
import pandas as pd
import json
from datetime import datetime
import pytest
import io


def determine_testing_result(pytest_output):
    """
    Automate reading the pytest output to determine if the tests passed, the tests failed, or if there was
    a runtime error.
    Args:
        pytest_output: The output of pytest as a string.
    Returns:
        -1 if the test code has a runtime error,
        0 if the tests ran but failed on the code or if it's a type of error listed below for a specific function.
        and 1 if the tests ran and passed on the code
        there are some expectations!
    """
    # Check for other AssertionErrors
    if "AssertionError" in pytest_output:
        return 0

    if "TypeError" in pytest_output:
        if "not supported between instances of" in pytest_output:
            return -1
        return 0

    if "ValueError" in pytest_output:
        if "NameError: name 'pytest' is not defined" in pytest_output:
            return -1
        return 0

    # List of specific error types for runtime errors
    error_types = ["NameError", "ZeroDivisionError", "IndexError", "ImportError", "KeyError", "AttributeError"]

    # Check for known runtime errors
    for error in error_types:
        if error in pytest_output:

            if "pytest.raises" in pytest_output:
                return 0

            if f"raise {error}" in pytest_output:
                return 0

            return -1

    # Handle xpass or xfail conditions as test failures
    if "xpass" in pytest_output:
        return 0

    elif "failed" not in pytest_output and "passed" in pytest_output:
        return 1

    elif "xfail" in pytest_output and "passed" in pytest_output:
        return 1

    else:
        return -1


def execute_pytest_without_printing(test_dir):
    """
    Runs pytest on all files in the specified test directory and stores the output of pytest. The output is not
    printed to the screen and is returned.
    Args:
        test_dir (str):  the path to the test directory

    Returns: the output from running pytest as a string.

    """
    # Run pytest using subprocess
    # subproc_result = subprocess.run(["pytest", "-x", test_dir, "--capture",
    #                                 "sys", "-v", "--cache-clear"],
    #                                shell=True, capture_output=True, text=True)
    #
    # pytest_output = subproc_result.stdout
    original_output = sys.stdout
    sys.stdout = io.StringIO()
    pytest_args = [
        "-x", test_dir, "--capture", "sys", "-v",
        "--cache-clear"
    ]
    pytest.main(pytest_args)
    pytest_output = sys.stdout.getvalue()
    sys.stdout.close()
    # Reset original standard output
    sys.stdout = original_output

    return pytest_output


def run_pytest_on_code(curr_test_dir, verbose):
    if not os.path.isdir(curr_test_dir):
        os.makedirs(curr_test_dir)
    os.chdir(curr_test_dir)
    if os.path.exists(os.path.join(curr_test_dir, "__pycache__")) and \
            os.path.isdir(os.path.join(curr_test_dir, "__pycache__")):
        shutil.rmtree(os.path.join(curr_test_dir, "__pycache__"))
    if os.path.exists(os.path.join(curr_test_dir, ".pytest_cache")) and \
            os.path.isdir(os.path.join(curr_test_dir, ".pytest_cache")):
        shutil.rmtree(os.path.join(curr_test_dir, ".pytest_cache"))
    correct_pytest_output = execute_pytest_without_printing(curr_test_dir)
    if verbose:
        print("**Pytest output on code**")
        print(correct_pytest_output)
    if os.path.exists(os.path.join(curr_test_dir, "__pycache__")) and \
            os.path.isdir(os.path.join(curr_test_dir, "__pycache__")):
        shutil.rmtree(os.path.join(curr_test_dir, "__pycache__"))
    if os.path.exists(os.path.join(curr_test_dir, ".pytest_cache")) and \
            os.path.isdir(os.path.join(curr_test_dir, ".pytest_cache")):
        shutil.rmtree(os.path.join(curr_test_dir, ".pytest_cache"))
    return correct_pytest_output


def is_json_correct(filepath):
    """
    Checks to see if a filepath is a valid JSON, if yes returns true if not returns false
    Args:
        filepath: a filepath

    Returns: boolean - Trye or False

    """

    if os.path.exists(filepath):
        with open(filepath) as f:
            json.load(f)
        return True
    else:
        return False


def is_file_valid(json_filepath):
    """
    Checks to see if a submission file path or problem filepath is a valid JSON, if yes returns true if not returns
    false
    Args:
        json_filepath: a filepath where a JSON file is

    Returns: boolean - True or False

    """
    json_set = open(json_filepath, "r")
    json_data = json.load(json_set)

    code_files = json_data['code_list']

    for problem in code_files:
        if "trial_id" not in problem:
            print(f"Problem\n{problem}\ndoes not contain a trial_id key value, please fix this!\n")
            return False
        else:
            continue


def is_filepath_and_submission_correct(problem_file_path, submission_file_path):
    """
    Checks to see if a submission file and problem file match - if not will return false
    Args:
        submission_file_path: a filepath where a JSON file is
        problem_file_path: a filepath where a problem JSON file is

    Returns: boolean - True or False

    """
    value = True
    counter_submission = 0
    counter_problem = 0

    submission_set = open(submission_file_path, "r")
    submission_data = json.load(submission_set)
    submission_elements = submission_data['code_list']

    problem_set = open(problem_file_path, "r")
    problem_data = json.load(problem_set)
    problem_elements = problem_data['code_list']

    for submission_field in submission_elements:
        if (submission_field["prompt_number"] == "0"):
            counter_submission = counter_submission + 1

    for problem_field in problem_elements:
        counter_problem = counter_problem + 1

    if (counter_submission != counter_problem):
        value = False

    return value


def is_submission_field_empty(submission_file_path):
    """
    Checks to see if a submission file does not have any empty fields - if yes will return false
    Args:
        submission_file_path: a filepath where a JSON file is

    Returns: boolean - True or False

    """
    value = True
    submission_set = open(submission_file_path, "r")
    submission_data = json.load(submission_set)

    submission_elements = submission_data['code_list']

    for submission_field in submission_elements:
        if ("trial_id" not in submission_field or "prompt_number" not in submission_field or "prompt" not
                in submission_field or "test_output" not in submission_field or "primary_method_name" not in
                submission_field or "test_code" not in submission_field):
            print(f"Problem\n{submission_field}\nis missing either a trial_id and or prompt_number and or prompt "
                  f"and or primary_method_name and or test_output and or test_code\n")
            value = False

        elif (len(submission_field['trial_id']) == 0 or len(submission_field['prompt_number']) == 0 or
                len(submission_field['prompt']) == 0 or len(submission_field['test_output']) == 0 or
                len(submission_field['primary_method_name']) == 0 or len(submission_field['test_code']) == 0):
            print(f"Problem\n{submission_field}\nis missing either a value for trial_id and or prompt_number and or "
                  f"prompt and or primary_method_name and or test_output and or test_code\n")
            value = False
        else:
            value = True

    return value


def is_prompt_num_str(submission_file_path):
    """
    Checks to see if a submission file does not have any empty fields - if yes will return false
    Args:
        submission_file_path: a filepath where a JSON file is

    Returns: boolean - True or False

    """
    value = True
    submission_set = open(submission_file_path, "r")
    submission_data = json.load(submission_set)

    submission_elements = submission_data['code_list']

    for submission_field in submission_elements:
        if not isinstance(submission_field['prompt_number'], str):
            print(f"Problem\n{submission_field}\nprompt number is not a string. Please recheck and try again!\n")
            value = False
        else:
            value = True

    return value


def control_submission_output(submission_file_path):
    """
    Checks to see if a submission file code is not more than 25000 character, if it is returns an error
    Args:
        submission_file_path: a filepath where a JSON file is

    Returns: boolean - True or False

    """
    submission_set = open(submission_file_path, "r")
    submission_data = json.load(submission_set)

    submission_elements = submission_data['code_list']
    value = True

    for submission_field in submission_elements:
        if len(submission_field['test_code']) > 25000:
            print("The test code for " + submission_field['trial_id']
                  + "_" + submission_field['prompt_number'] + " is too long, please recheck and try again!\n")
            value = False
        else:
            value = True

    return value


def is_prompt_correct(submission_file_path, problem_file_path):
    """
    Checks to see if a submission file has a valid prompt number. For prompt number 1, it is a fixed prompt. If
    fixed prompt, checks to see if the prompt is the same fixed prompt we have given, if this is true will return
    true. If prompt number is 1 - 9, it is a custom prompt, need to make sure each submission has at least one
    custom prompt per problem. If all this matches returns true. If prompt number or prompt for fixed prompt is
    something else, returns false.
    Args:
        submission_file_path: a filepath where a submission JSON file is
        problem_file_path: a filepath where a problem JSON file is

    Returns: boolean - True or False

    """
    submission_set = open(submission_file_path, "r")
    submission_data = json.load(submission_set)
    submission_elements = submission_data['code_list']

    problem_set = open(problem_file_path, "r")
    problem_data = json.load(problem_set)
    problem_elements = problem_data['code_list']
    fixed_prompt = []
    custom_prompt = []
    problems = []
    value = False

    for submission_field in submission_elements:
        try:
            code_data_list = [x for x in problem_elements if x["trial_id"] == submission_field["trial_id"]]
            code_data = code_data_list[0]
        except IndexError:
            print("One or more problems in the submission does not exist in the problem file, just ignore "
                  "this\n")

        if int(submission_field["prompt_number"]) == 0:
            fixed_prompt.append(submission_field['trial_id'])
            if code_data["prompt_fixed"] == submission_field["prompt"]:
                value = True
            else:
                print(f"This {submission_field['trial_id']} is not a fixed prompt, either the prompt number is not 0 "
                      f"or the submission prompt does not match the prompt we gave you, please recheck and try "
                      f"again!.\n")
                return False

        elif int(submission_field["prompt_number"]) == 1:
            custom_prompt.append(submission_field['trial_id'])
            if (code_data["prompt_fixed"] == submission_field["prompt"] or code_data["prompt_fixed"] !=
                    submission_field["prompt"]):
                print(f"This {submission_field['trial_id']}_{submission_field['prompt_number']} is not a fixed prompt, "
                      f"it is a custom prompt.\n")
                value = True

        elif 1 < int(submission_field["prompt_number"]) < 10:
            print(f"This {submission_field['trial_id']}_{submission_field['prompt_number']} is not a fixed prompt, "
                  f"it is a custom prompt.\n")
            value = True

        else:
            print(f"This {submission_field['trial_id']} does not have a valid prompt number.\nPlease make sure the "
                  f"fixed prompt_number is {"0"} and the custom prompt_number is a number from {1} to {9}, "
                  f"please recheck and try again!.\n")
            return False

    for problem in problem_elements:
        problems.append(problem["trial_id"])

    length = len(problems)

    if len(fixed_prompt) != length:
        print(f"There is not a fixed prompt per problem or too many fixed prompts per problem, look through the "
              f"problems\n{fixed_prompt}\nmake the fix and resubmit!\n")
        return False
    elif len(custom_prompt) < length:
        print(f"There is not a custom prompt per problem. Please make sure the first custom prompt,\nprompt_number is"
              f" {1}, look through the problems, make the fix and resubmit!\n")
        return False
    elif len(custom_prompt) > (9 * length):
        print("There are too many custom prompt per problem, look through the problems, make the fix "
              "and resubmit!\n")
        return False

    return value


def validate_code_submission(str_current_datetime, prob_json_filepath,
                             submission_json_filepath, temp_test_dir,
                             output_dir, system_name, verbose):
    """
    Validates the submitted json file of generated tests relative to the problem json file. Prints out errors with
    "ERROR: ..." and warnings with "WARNINGS: ..." Warnings can be ignored but often indicate a problem with the
    submission. However, a submission must be free of all errors to pass validation.

    Args:
        str_current_datetime (datetime): The date and time provided. If this is "" (default), then automatically
        create the current date and time. This parameter is enabled so that if someone wishes to overwrite previous
        output in a folder, that previous date can be specified. By default, leave "".
        prob_json_filepath (str): The path to the problem json file.
        submission_json_filepath (str): The path to the submission json file
        temp_test_dir (str): The path to the temporary directory where test files can be created and deleted
        output_dir: The directory to write the output to
        system_name: The name of the system. Defaults to "", which means that the system name will be
                     extracted from the submission json.
        verbose (bool): True if verbose output is enabled. False otherwise.

    Returns: The validator outputs as a bool. If the validation is successful, it will return True if not it will
    return False.

    """

    is_submission_valid = True
    no_trial_id_list = []

    # Make output directory with current date for time-stamped outputs
    if str_current_datetime == "":
        current_datetime = datetime.now().strftime("%Y-%m-%d-T%H-%M-%S")
        str_current_datetime = str(current_datetime)
    folder_name = str_current_datetime + "-outputs"
    out_folder_fp = os.path.join(output_dir, folder_name)
    if not os.path.isdir(out_folder_fp):
        os.makedirs(out_folder_fp)

    log_filepath = os.path.join(out_folder_fp, "validation_log.txt")
    with (open(log_filepath, "w") as log_file):

        # Checking to see if the file exists and correctly formatted
        if is_json_correct(prob_json_filepath) != True or is_json_correct(submission_json_filepath) != True:
            is_submission_valid = False
            if not is_submission_valid:
                print(f"ERROR: Either the problem file:{prob_json_filepath}\nor submission file:"
                      f"{submission_json_filepath}\n"
                      f"is not a correctly formatted json, please recheck and try again!")
                print("============================================")
                print("Final Result: ERROR - Submission Failed Validation! Please see output and fix all validation "
                      "errors.")
                print("============================================")

            elif verbose:
                print(f"ERROR: Either the problem file:{prob_json_filepath}\nor submission file:"
                      f"{submission_json_filepath}\n is not a correctly formatted json, please recheck and try "
                      f"again!")
                print("============================================")
                print("Final Result: ERROR - Submission Failed Validation! Please see output and fix all validation "
                      "errors.")
                print("============================================")

            log_file.write(f"ERROR: Either the problem file:{prob_json_filepath}\nor submission file:"
                           f"{submission_json_filepath}\n is not a correctly formatted json, "
                           f"please recheck and try again!\n")

            return is_submission_valid

        # Load json files with the key metadata for the problemset
        problem_set = open(prob_json_filepath, "r")
        problem_data = json.load(problem_set)
        problem_set.close()
        problem_df = pd.DataFrame.from_dict(problem_data['code_list'], orient="columns")

        # Load json files with the submission
        submission_set = open(submission_json_filepath, "r")
        submission_data = json.load(submission_set)
        submission_set.close()
        submission_df = pd.DataFrame.from_dict(submission_data['code_list'], orient="columns")
        sys_name = str(system_name)
        if sys_name == "":
            sys_name = submission_data['system']
        else:
            submission_data['system'] == sys_name
        submission_df['system'] = sys_name

        submission_dirpath = os.path.join(out_folder_fp, sys_name)
        if not os.path.isdir(submission_dirpath):
            os.makedirs(submission_dirpath)
        # Set working directory to test directory
        prev_wd = os.getcwd()
        if verbose:
            print("Previous Working Directory: {}".format(prev_wd))
        os.chdir(temp_test_dir)
        # curr_test_dir = temp_test_dir

        submission_elements = submission_data['code_list']
        problem_elements = problem_data['code_list']

        # Checking to see if the problem file and submission file have a trial_id field if not, will cause an error
        if is_file_valid(prob_json_filepath) == False or is_file_valid(submission_json_filepath) == False:
            is_submission_valid = False
            print("ERROR: Missing or do not have a trial_id in one or more problems in submission file, "
                  "please recheck and try again!")
            print("============================================")
            print("Final Result: ERROR - Submission Failed Validation! Please see output and fix all validation "
                  "errors.")
            print("============================================")

            log_file.write("ERROR: Missing or do not have a trial_id in one or more problems in submission "
                           "file, please recheck and try again!\n")
            return is_submission_valid

        # Checking to see the problems in the submission file, if submission file has problem that are not in the
        # input file, skips over problem
        for submission in submission_elements:
            submission_task = submission['trial_id']
            if not (submission_task in problem_df['trial_id'].to_list()):
                print(f"WARNING: Task {submission_task} not in problem file\n{prob_json_filepath}.\n"
                      f"Skipping the tests for this program.\n")

                log_file.write(f"WARNING: Task {submission_task} not in problem file\n{prob_json_filepath}.\n"
                               f"Skipping the tests for this program.\n")

        # Checking to see the problems in the submission file, if submission file is missing any problems that are
        # in the input file causes an error
        for problem in problem_elements:
            problem_task = problem['trial_id']
            if not (problem_task in submission_df['trial_id'].to_list()):
                is_submission_valid = False
                if not is_submission_valid:
                    print(f"ERROR: Task {problem_task} not in submission file {submission_json_filepath}, "
                          f"please recheck and try again!")
                    print("============================================")
                    print(
                        "Final Result: ERROR - Submission Failed Validation! Please see output and fix all validation "
                        "errors.")
                    print("============================================")

                no_trial_id_list.append(problem_task)

                log_file.write(f"ERROR: Task {problem_task} not in submission file "
                               f"{submission_json_filepath}, please recheck and try again!\n")

        if len(no_trial_id_list) > 0:
            is_submission_valid = False
            return is_submission_valid

        # Checking to see if the submission file match the input problem file
        if not is_filepath_and_submission_correct(prob_json_filepath, submission_json_filepath):
            is_submission_valid = False
            if not is_submission_valid:
                print(f"ERROR: The submission problems: {submission_json_filepath}\ndo not match the problems in the "
                      f"problem file: {prob_json_filepath}.\nEither they are different problems or there is more than "
                      f"one fixed prompt per problem. Please recheck and try again!")
                print("============================================")
                print("Final Result: ERROR - Submission Failed Validation! Please see output and fix all validation "
                      "errors.")
                print("============================================")

            log_file.write(f"ERROR: The submission problems: {submission_json_filepath}\ndo not match the problems in "
                           f"the problem file: {prob_json_filepath}.\nEither they are different problems or there is "
                           f"more than one fixed prompt per problem. Please recheck and try again!")

            return is_submission_valid

        # Checking to see if the fixed prompt is correct
        if not is_prompt_correct(submission_json_filepath, prob_json_filepath):
            is_submission_valid = False
            if not is_submission_valid:
                print("ERROR: Please recheck the prompt and or prompt_number field, one of these are incorrect, "
                      "please fix and try again!")
                print("============================================")
                print("Final Result: ERROR - Submission Failed Validation! Please see output and fix all validation "
                      "errors.")
                print("============================================")

            log_file.write("ERROR: Please recheck the prompt and or prompt_number field, one of these are incorrect, "
                           "please fix and try again!\n")

            return is_submission_valid

        # Checking to see if the submission file prompt number is a string, if not will cause an error
        if not is_prompt_num_str(submission_json_filepath):
            is_submission_valid = False
            if not is_submission_valid:
                print(
                    f"ERROR: The prompt number in the submission file\n{submission_json_filepath}\nis not a string "
                    f"please recheck and try again!")
                print("============================================")
                print(
                    "Final Result: ERROR - Submission Failed Validation! Please see output and fix all validation "
                    "errors.")
                print("============================================")

            log_file.write(
                f"ERROR: The prompt number in the submission file\n{submission_json_filepath}\nis not a string "
                f"please recheck and try again!")

            return is_submission_valid

        # Checking to see if the submission file have the correct fields if not, will cause an error
        if not is_submission_field_empty(submission_json_filepath):
            is_submission_valid = False
            if not is_submission_valid:
                print(f"ERROR: One or more fields in the submission file\n{submission_json_filepath}\nis or are "
                      f"empty, please recheck and try again!")
                print("============================================")
                print("Final Result: ERROR - Submission Failed Validation! Please see output and fix all validation "
                      "errors.")
                print("============================================")

            log_file.write(f"ERROR: One or more fields in the submission file\n{submission_json_filepath}\nis or are "
                           f"empty, please recheck and try again!\n")

            return is_submission_valid

        # Checking to see if the submission file test code has too many characters, if so will cause an error
        if not control_submission_output(submission_json_filepath):
            is_submission_valid = False
            if not is_submission_valid:
                print(f"ERROR: The test code for one or more problems in\n{submission_json_filepath}\nis or are too "
                      f"long, please recheck and try again!")
                print("============================================")
                print("Final Result: ERROR - Submission Failed Validation! Please see output and fix all validation "
                      "errors.")
                print("============================================")

            log_file.write(f"ERROR: The test code for one or more problems in\n{submission_json_filepath}\nis or are "
                           f"too long, please recheck and try again!\n")

            return is_submission_valid

        # If verbose, write the submitted output to a file
        if verbose:
            subm_val_fp = os.path.join(submission_dirpath, "{}_validation.csv".format(sys_name))
            submission_df.to_csv(subm_val_fp, index=False)
            print("Results of Running Tests on Provided Code:")
            print(submission_df.loc[:, ["system", "trial_id"]])

        if is_submission_valid:
            log_file.write(f"Your submission\n{submission_json_filepath}\nis valid!")
            print()
            print("============================================")
            print("Final Result: SUCCESS - Submission Successfully Validated!")
            print("============================================")
            print(f"If you want more information, look at the log created here:\n{log_filepath}")
            print("============================================")

        else:
            print()
            print("============================================")
            print("Final Result: ERROR - Submission Failed Validation! Please see output and fix all validation "
                  "errors.")
            print(f"If you want more information, look at the log created here:\n{log_filepath}")
            print("============================================")

        log_file.close()
        return is_submission_valid


def code_main(args):
    config_filepath = args.config_filepath
    config_mode = args.config_mode
    input_json_filepath = args.input_filepath
    submission_filepath = args.submission_filepath
    temp_working_dir = args.temp_working_dir
    output_dir = args.output_dir
    str_current_datetime = args.datetime_for_dir
    system_name = args.system_name
    verbose = args.verbose
    print("||| Script: evaluate_submission.py json file")

    if verbose:
        print("Args:")
        print("||| Config File Used: {}".format(config_filepath))
        print("||| Config mode: {}".format(config_mode))
        print("||| Input Problem json filepath: {}".format(input_json_filepath))
        print("||| Submission Filepath: {}".format(submission_filepath))
        print("||| Output Directory: {}".format(output_dir))
        print("||| Temp Working Directory: {}".format(temp_working_dir))
        print("||| Datetime Str: {}".format(str_current_datetime))
        print("||| System Name: {}".format(system_name))
    # Show what the verbose option is
    print("||| Verbose Option: {}. Set verbose to True to print more information".format(verbose))

    result = validate_code_submission(
        str_current_datetime=str_current_datetime,
        prob_json_filepath=input_json_filepath,
        submission_json_filepath=submission_filepath,
        temp_test_dir=temp_working_dir,
        output_dir=output_dir,
        system_name=system_name,
        verbose=verbose
    )

    # For the web platform: exit if the result is False.
    if not result:
        sys.exit(1)


def define_parser():
    """
    Defines accepted CLI syntax and the actions to take for command and args.

    Returns:
        argparse parser

    """
    default_config_filepath = os.environ["GENAI_CODE_CONFIG_PATH"]
    default_config_mode = "Pilot1Evaluator"

    # Now extract the arguments from the config file
    try:
        config = configparser.ConfigParser()
        with open(default_config_filepath) as configfile:
            config.read_file(configfile)
    except ImportError:
        sys.exit("Cannot open config file: " + default_config_filepath)

    # Read root directories from config file
    # root_repo_dir = config[config_mode]["root_repo_dir"]
    root_working_dir = config[default_config_mode]["root_working_dir"]
    default_temp_working_dir = os.path.join(root_working_dir)

    default_datetime_str = ""
    default_system_name = ""

    parser = argparse.ArgumentParser(description="Validate Test-Code Generating Systems")

    parser.add_argument(
        "-f",
        "--config_filepath",
        help="Location of Configuration file",
        required=False,
        type=str,
        default=default_config_filepath,
    )
    parser.add_argument(
        "-m", "--config_mode", help="Mode of Configuration_file", required=False, type=str, default=default_config_mode
    )
    parser.add_argument(
        "-s",
        "--submission_filepath",
        help="Absolute Path to submission json file.",
        required=True,
        type=str
    )
    parser.add_argument(
        "-i",
        "--input_filepath",
        help="Absolute path to input problem file.",
        required=True,
        type=str
    )
    parser.add_argument(
        "-y",
        "--system_name",
        help="System Name",
        required=False,
        type=str,
        default=default_system_name,
    )
    datetime_help_str = """ Datetime-string to use for datetime for folders. Put "" to have program make its own'
                              Format as (Y)-(m)-(d)-T(H)-(M)-(S).
                          """
    parser.add_argument(
        "-d", "--datetime_for_dir", help=datetime_help_str, required=False, type=str, default=default_datetime_str
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        help="Absolute path to the output directory.",
        required=True,
        type=str
    )
    parser.add_argument(
        "-w",
        "--temp_working_dir",
        help="Absolute path to the temporary working directory.",
        required=False,
        type=str,
        default=default_temp_working_dir,
    )
    parser.add_argument(
        "-v", "--verbose", help="Enable Verbose output", required=False, action="store_true", default=False
    )

    # This tells the code to automatically execute this function
    parser.set_defaults(func=code_main)
    return parser


def main():
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    pd.set_option("display.max_colwidth", 200)
    parser = define_parser()
    args = parser.parse_args()
    if hasattr(args, "func") and args.func is not None:
        args.func(args)
    else:
        parser.print_help()

    # `code_main(args)` is automatically called


if __name__ == "__main__":
    main()
