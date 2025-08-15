#! /usr/bin/env python
# Code to run submission test on correct version of front_times_input
import configparser
import os
import shutil
import sys
import argparse
import pandas as pd
import numpy as np
import json
from datetime import datetime
import re
import subprocess

# Use pytest modules from validation file to avoid duplications
from genai_code_test.evaluation_environment.validate_submission import (
    determine_testing_result,
    execute_pytest_without_printing,
    run_pytest_on_code,
)


def mean_metrics_dataframe(dataframe, subm_system_name):

    final = []
    group_df = dataframe.groupby('prompt_number')

    for prompt_num, group_prompt_num in group_df:
        total_problems = len(group_prompt_num['trial_id'])

        total_problems_for_mean_coverage = (group_prompt_num['correct_tests'] == 1).sum()

        # getting information
        for_perc_tc_value = group_prompt_num[(group_prompt_num['correct_tests'] == 1)]

        for_perc_tc_fi1_value = group_prompt_num[(group_prompt_num['correct_tests'] == 1) &
                                                 (group_prompt_num['finds_error_in_incorrect_1'] == 1)]

        for_perc_tc_fi1_fit_value = group_prompt_num[(group_prompt_num['correct_tests'] == 1) &
                                                     (group_prompt_num['finds_error_in_incorrect_1'] == 1) &
                                                     (group_prompt_num['finds_error_in_incorrect_t'] == 1)]

        for_perc_tc_fit_value = group_prompt_num[(group_prompt_num['correct_tests'] == 1) &
                                                 (group_prompt_num['finds_error_in_incorrect_t'] == 1)]

        code_coverage_100 = group_prompt_num[(group_prompt_num['correct_tests'] == 1) &
                                             (group_prompt_num['finds_error_in_incorrect_1'] == 1) &
                                             (group_prompt_num['finds_error_in_incorrect_t'] == 1) &
                                             (group_prompt_num['code_coverage'] == 100)]

        average_code_coverage = group_prompt_num.loc[(group_prompt_num['correct_tests'] == 1) &
                                                     (group_prompt_num[
                                                         'code_coverage'].notnull()), 'code_coverage'].tolist()

        # computing values
        perc_tc = (len(for_perc_tc_value) / total_problems) * 100
        perc_tc_fi1 = (len(for_perc_tc_fi1_value) / total_problems) * 100
        perc_tc_fi1_fit = (len(for_perc_tc_fi1_fit_value) / total_problems) * 100
        perc_tc_fit = (len(for_perc_tc_fit_value) / total_problems) * 100
        perc_tc_fi1_fit_hcov = (len(code_coverage_100) / total_problems) * 100
        mean_coverage = sum(average_code_coverage) / total_problems_for_mean_coverage if (
            total_problems_for_mean_coverage > 0) else 0

        result = {
            "system": subm_system_name,
            "prompt_number": prompt_num,
            "correct_tests": perc_tc,
            "finds_ci1_error": perc_tc_fi1,
            "finds_ci1_and_cit_errors": perc_tc_fi1_fit,
            "finds_cit_error": perc_tc_fit,
            "full_coverage_and_finds_all_errors": perc_tc_fi1_fit_hcov,
            "mean_coverage": mean_coverage,


        }
        final.append(result)

    final_df = pd.DataFrame(final)
    return final_df


def run_pytest_and_coverage_on_code(curr_test_dir, output_dir, file_suffix, task, verbose):
    """
    Runs pytest and coverage on the code and tests using the code and tests as specified in curr_test_dir.  Coverage
    is only run if the pytest on the code is correct

    Args:
        curr_test_dir: path to the directory where the code and tests are located
        output_dir: path to the directory to write test and coverage outputs to.
        file_suffix: the suffix of the file name to add to output files. This is often constructed from the trial_id.
        task: the name of the task or the trial
        verbose: A True/False boolean flag if verbose output should be printed or not.

    Returns: a tuple with the (coverage_pytest_output, total_coverage_percentage). Additionally, relevant outputs are
    written to the directory output_dir.

    """
    # cov_fname = "genai_code_file" + "_" + file_suffix + ".py"
    if os.path.exists(os.path.join(curr_test_dir, "__pycache__")) and \
            os.path.isdir(os.path.join(curr_test_dir, "__pycache__")):
        shutil.rmtree(os.path.join(curr_test_dir, "__pycache__"))
    if os.path.exists(os.path.join(curr_test_dir, ".pytest_cache")) and \
            os.path.isdir(os.path.join(curr_test_dir, ".pytest_cache")):
        shutil.rmtree(os.path.join(curr_test_dir, ".pytest_cache"))

    coverage_pytest_output = execute_pytest_without_printing(curr_test_dir)

    if verbose:
        print("**Pytest output**")
        print(coverage_pytest_output)

    coverage_test_status = determine_testing_result(coverage_pytest_output)
    total_cov = np.nan
    if coverage_test_status == 1:
        if verbose:
            print("**Generating Coverage Report**")
        htmlcov_dirpath = os.path.join(output_dir, file_suffix + "_htmlcov")
        if not os.path.isdir(htmlcov_dirpath):
            os.makedirs(htmlcov_dirpath)
        command_str = (f"coverage run -m pytest {curr_test_dir} -x --capture sys -v --cache-clear; "
                       f"coverage report; "
                       f"coverage html --include -d {htmlcov_dirpath}")
        coverage_out = subprocess.run(command_str, shell=True,
                                      capture_output=True, text=True)
        total_cov = 0.0
        for line in coverage_out.stdout.split("\n"):
            if "TOTAL" in line:
                total_cov = float(line.split()[3][:-1])
                break
    else:
        if verbose:
            print("No Code Coverage because tests failed")

    # Delete temp-created files
    if os.path.exists(os.path.join(curr_test_dir, "__pycache__")) and os.path.isdir(
        os.path.join(curr_test_dir, "__pycache__")
    ):
        shutil.rmtree(os.path.join(curr_test_dir, "__pycache__"))
    if os.path.exists(os.path.join(curr_test_dir, ".pytest_cache")) and os.path.isdir(
        os.path.join(curr_test_dir, ".pytest_cache")
    ):
        shutil.rmtree(os.path.join(curr_test_dir, ".pytest_cache"))
    if os.path.exists(os.path.join(curr_test_dir, ".coverage")):
        os.remove(os.path.join(curr_test_dir, ".coverage"))
    # Return pytest output and coverage percentage
    return coverage_pytest_output, total_cov


def evaluate_code_submission(
    str_current_datetime, key_json_filepath, submission_json_filepath, temp_test_dir, output_dir,
        system_name, verbose
):
    """
    Evaluates and scores a code submission.

    Args:
        str_current_datetime: The string of the current date and time to use to create a directory. Should be
            specified in "%Y-%m-%d-T%H-%M-%S". The default is "", which if empty, this method will use the
            current date and time.
        key_json_filepath: The absolute path to the key json file.
        submission_json_filepath: The absolute path to the submission json file.
        temp_test_dir: The absolute path to the temporary directory that can be used to create and delete test files
        output_dir: The absolute path to the output directory where the scoring output should be written.
        system_name: The name of the system. Defaults to "", which means that the system name will be
                     extracted from the submission json.
        verbose: A True/False boolean flag if verbose output should be printed or not.

    Returns: None. Any outputs are written to the directory specified by output_dir.

    """
    # Make output directory with current date for time-stamped outputs

    value = True

    if str_current_datetime == "":
        current_datetime = datetime.now().strftime("%Y-%m-%d-T%H-%M-%S")
        str_current_datetime = str(current_datetime)
    folder_name = str_current_datetime + "-outputs"
    out_folder_fp = os.path.join(output_dir, folder_name)
    if not os.path.isdir(out_folder_fp):
        os.makedirs(out_folder_fp)

    # Load json files with the key metadata for the problemset
    key_f = open(key_json_filepath, "r")
    key_data = json.load(key_f)
    key_f.close()
    key_df = pd.DataFrame.from_dict(key_data["code_list"], orient="columns")
    # Load json files with the submission
    subm_f = open(submission_json_filepath, "r")
    subm_data = json.load(subm_f)
    subm_f.close()
    subm_df = pd.DataFrame.from_dict(subm_data["code_list"], orient="columns")
    sys_name = str(system_name)
    if sys_name == "":
        sys_name = subm_data["system"]
    else:
        subm_data["system"] = sys_name
    short_sys_name = sys_name.replace(" ", "_")

    if len(short_sys_name) >= 5:
        short_sys_name = short_sys_name[0:5]
    else:
        short_sys_name = short_sys_name
    subm_df["system"] = sys_name
    subm_df["correct_tests"] = ""
    subm_df["finds_error_in_incorrect_1"] = ""
    subm_df["finds_error_in_incorrect_t"] = ""
    subm_df["code_coverage"] = np.nan

    subm_dirpath = os.path.join(out_folder_fp, sys_name)
    if not os.path.isdir(subm_dirpath):
        os.makedirs(subm_dirpath)
    # Set working directory to test directory
    prev_wd = os.getcwd()
    if verbose:
        print("Previous Working Directory: {}".format(prev_wd))
    os.chdir(temp_test_dir)
    curr_test_dir = temp_test_dir
    # Mek subfolders in test directory
    # outer_wd = os.getcwd()
    # sys_test_dir = os.path.join(temp_test_dir, sys_name)
    # if not os.path.isdir(sys_test_dir):
    #     os.makedirs(sys_test_dir)
    elements = subm_data["code_list"]
    for e in elements:
        task = e["trial_id"]
        prompt_number = e['prompt_number']

        # Check that this is a task in the problem set; skip it if not
        if not (task in key_df["trial_id"].to_list()):
            print("Task {} not in problem set {}. Skipping this task.".format(task, key_json_filepath))
            continue
        correct_code = key_df.loc[key_df["trial_id"] == task, "code_correct"].iloc[0]
        # This line is a temporary fix so that the code works with this version of the key
        task_code = task.replace(" ", "_")
        # Replace correct code with import
        if int(prompt_number) == 0:
            correct_file_suffix = (task_code + "_" + str(prompt_number) + "_" + str(short_sys_name) + "_correct_fixed")
            correct_code_fname = "genai_code_file" + "_" + correct_file_suffix + ".py"

            mutated_code = key_df.loc[key_df["trial_id"] == task, "code_incorrect_1"].iloc[0]
            mutated_file_suffix = (task_code + "_" + str(prompt_number) + "_" + str(short_sys_name) +
                                   "_incorrect_fixed")
            mutated_code_fname = "genai_code_file" + "_" + mutated_file_suffix + ".py"

            mutated_code_t = key_df.loc[key_df["trial_id"] == task, "code_incorrect_t"].iloc[0]
            mutated_file_suffix_t = (task_code + "_" + str(prompt_number) + "_" + str(short_sys_name) +
                                     "_incorrect_t_fixed")
            mutated_code_fname_t = "genai_code_file" + "_" + mutated_file_suffix_t + ".py"

        elif 0 < int(prompt_number) < 10:
            correct_file_suffix = (task_code + "_" + str(prompt_number) + "_" + str(short_sys_name) + "_correct_custom")
            correct_code_fname = "genai_code_file" + "_" + correct_file_suffix + ".py"

            mutated_code = key_df.loc[key_df["trial_id"] == task, "code_incorrect_1"].iloc[0]
            mutated_file_suffix = (task_code + "_" + str(prompt_number) + "_" + str(short_sys_name) +
                                   "_incorrect_custom")
            mutated_code_fname = "genai_code_file" + "_" + mutated_file_suffix + ".py"

            mutated_code_t = key_df.loc[key_df["trial_id"] == task, "code_incorrect_t"].iloc[0]
            mutated_file_suffix_t = (task_code + "_" + str(prompt_number) + "_" + str(short_sys_name) +
                                     "_incorrect_t_custom")
            mutated_code_fname_t = "genai_code_file" + "_" + mutated_file_suffix_t + ".py"

        sys_test_code = e["test_code"]
        # Making a deeper working directory for the task
        # task_test_dir = os.path.join(sys_test_dir, task)
        # if not os.path.isdir(task_test_dir):
        #     os.makedirs(task_test_dir)
        # os.chdir(task_test_dir)
        # curr_test_dir = os.path.join(task_test_dir, "correct")

        # Creating output directory structure to provide output results.
        # Crate a directory for the task
        task_output_dirpath = os.path.join(subm_dirpath, task)
        if not os.path.isdir(task_output_dirpath):
            os.makedirs(task_output_dirpath)

        # # **Correct Code Case*** Test submitted code on the (correct) version of the input code
        # # **Correct Code Case***
        # Make temp files for code and test code
        correct_code_fp = os.path.join(curr_test_dir, correct_code_fname)
        testc_code_fname = "test_genai_code" + "_" + correct_file_suffix + ".py"
        testc_code_fp = os.path.join(curr_test_dir, testc_code_fname)
        sys_test_code_c = re.sub(r"genai_code_file", "genai_code_file" + "_" + correct_file_suffix, sys_test_code)
        with open(correct_code_fp, "w") as text_file:
            text_file.write(correct_code)
        with open(testc_code_fp, "w") as text_file:
            text_file.write(sys_test_code_c)
        correct_task_code_fp = os.path.join(task_output_dirpath, correct_code_fname)
        testc_task_code_fp = os.path.join(task_output_dirpath, testc_code_fname)
        with open(correct_task_code_fp, "w") as text_file:
            text_file.write(correct_code)
        with open(testc_task_code_fp, "w") as text_file:
            text_file.write(sys_test_code_c)

        # Run Pytest on Code
        # total_cov = 0
        # correct_pytest_output = run_pytest_on_code(curr_test_dir, task_output_dirpath)
        (correct_pytest_output, total_cov) = run_pytest_and_coverage_on_code(
            curr_test_dir, task_output_dirpath, correct_file_suffix, task, verbose
        )
        # subm_df.loc[subm_df['trial_id'] == task, 'code_coverage'] = total_cov
        correct_task_pytest_fp = os.path.join(task_output_dirpath, "pytest_output_" + correct_file_suffix + ".txt")
        with open(correct_task_pytest_fp, "w") as text_file:
            text_file.write(correct_pytest_output)
        correct_test_result = determine_testing_result(correct_pytest_output)
        subm_df.loc[subm_df["prompt_number"] == prompt_number, "prompt_number"] = prompt_number
        if correct_test_result == 1:
            subm_df.loc[(subm_df["trial_id"] == task) & (subm_df["prompt_number"] == prompt_number),
                        "correct_tests"] = 1
            subm_df.loc[(subm_df["trial_id"] == task) & (subm_df["prompt_number"] == prompt_number),
                        "code_coverage"] = total_cov
        elif correct_test_result == 0:
            subm_df.loc[(subm_df["trial_id"] == task) & (subm_df["prompt_number"] == prompt_number),
                        "correct_tests"] = 0
        else:
            subm_df.loc[(subm_df["trial_id"] == task) & (subm_df["prompt_number"] == prompt_number),
                        "correct_tests"] = -1
            value = False
        # Remove files in temp_test_dir
        os.remove(correct_code_fp)
        os.remove(testc_code_fp)

        # # **Mutated Code Case*** Test submitted code on the (mutated) version of the input code
        # # **Mutated Code Case***
        # Make temp files for code and test code
        if mutated_code == "":
            print("Skipping Mutated Code as mutated code does not exist")
            continue
        mutated_code_fp = os.path.join(curr_test_dir, mutated_code_fname)
        testm_code_fname = "test_genai_code" + "_" + mutated_file_suffix + ".py"
        testm_code_fp = os.path.join(curr_test_dir, testm_code_fname)
        sys_test_code_m = re.sub(r"genai_code_file", "genai_code_file" + "_" + mutated_file_suffix, sys_test_code)
        with open(mutated_code_fp, "w") as text_file:
            text_file.write(mutated_code)
        with open(testm_code_fp, "w") as text_file:
            text_file.write(sys_test_code_m)

        mutated_task_code_fp = os.path.join(task_output_dirpath, mutated_code_fname)
        testm_task_code_fp = os.path.join(task_output_dirpath, testm_code_fname)
        with open(mutated_task_code_fp, "w") as text_file:
            text_file.write(mutated_code)
        with open(testm_task_code_fp, "w") as text_file:
            text_file.write(sys_test_code_m)

        # Run Pytest on Code
        mutated_pytest_output = run_pytest_on_code(curr_test_dir, verbose)
        mutated_task_pytest_fp = os.path.join(task_output_dirpath, "pytest_output_" + mutated_file_suffix + ".txt")
        with open(mutated_task_pytest_fp, "w") as text_file:
            text_file.write(mutated_pytest_output)
        mutated_test_result = determine_testing_result(mutated_pytest_output)
        # Give full score if the tests fail on incorrect program,
        # i.e. we want mutated_test_result to be 0
        subm_df.loc[subm_df["prompt_number"] == prompt_number, "prompt_number"] = prompt_number
        if mutated_test_result == 1:
            subm_df.loc[(subm_df["trial_id"] == task) & (subm_df["prompt_number"] == prompt_number),
                        "finds_error_in_incorrect_1"] = 0
        elif mutated_test_result == 0:
            subm_df.loc[(subm_df["trial_id"] == task) & (subm_df["prompt_number"] == prompt_number),
                        "finds_error_in_incorrect_1"] = 1
        else:
            subm_df.loc[(subm_df["trial_id"] == task) & (subm_df["prompt_number"] == prompt_number),
                        "finds_error_in_incorrect_1"] = -1
            value = False
        # Remove files in temp_test_dir
        os.remove(mutated_code_fp)
        os.remove(testm_code_fp)
        # -- branch end

        # # **Mutated Code Case for Type error files *** Test submitted code on the (mutated) version of the input code
        # # **Mutated Code Case***
        # Make temp files for code and test code
        if mutated_code_t == "":
            print("Skipping Mutated Code as mutated code does not exist")
            continue
        mutated_code_fp_t = os.path.join(curr_test_dir, mutated_code_fname_t)
        testm_code_fname_t = "test_genai_code" + "_" + mutated_file_suffix_t + ".py"
        testm_code_fp_t = os.path.join(curr_test_dir, testm_code_fname_t)
        sys_test_code_m_t = re.sub(r"genai_code_file", "genai_code_file" + "_" + mutated_file_suffix_t, sys_test_code)
        with open(mutated_code_fp_t, "w") as text_file:
            text_file.write(mutated_code_t)
        with open(testm_code_fp_t, "w") as text_file:
            text_file.write(sys_test_code_m_t)

        mutated_task_code_fp_t = os.path.join(task_output_dirpath, mutated_code_fname_t)
        testm_task_code_fp_t = os.path.join(task_output_dirpath, testm_code_fname_t)
        with open(mutated_task_code_fp_t, "w") as text_file:
            text_file.write(mutated_code_t)
        with open(testm_task_code_fp_t, "w") as text_file:
            text_file.write(sys_test_code_m_t)

        # Run Pytest on Code
        mutated_pytest_output_t = run_pytest_on_code(curr_test_dir, verbose)
        mutated_task_pytest_fp_t = os.path.join(task_output_dirpath, "pytest_output_" + mutated_file_suffix_t + ".txt")
        with open(mutated_task_pytest_fp_t, "w") as text_file:
            text_file.write(mutated_pytest_output_t)
        mutated_test_result_t = determine_testing_result(mutated_pytest_output_t)
        # Give full score if the tests fail on incorrect program,
        # i.e. we want mutated_test_result to be 0
        subm_df.loc[(subm_df["prompt_number"] == prompt_number) & (subm_df["prompt_number"] == prompt_number),
                    "prompt_number"] = prompt_number
        if mutated_test_result_t == 1:
            subm_df.loc[(subm_df["trial_id"] == task) & (subm_df["prompt_number"] == prompt_number),
                        "finds_error_in_incorrect_t"] = 0
        elif mutated_test_result_t == 0:
            subm_df.loc[(subm_df["trial_id"] == task) & (subm_df["prompt_number"] == prompt_number),
                        "finds_error_in_incorrect_t"] = 1
        else:
            subm_df.loc[(subm_df["trial_id"] == task) & (subm_df["prompt_number"] == prompt_number),
                        "finds_error_in_incorrect_t"] = -1
            value = False

        # Remove files in temp_test_dir
        os.remove(mutated_code_fp_t)
        os.remove(testm_code_fp_t)
        # -- branch end
    # -- loop end

    # Write final submission data frame to output file
    subm_score_fp = os.path.join(subm_dirpath, "{}_scores.csv".format(sys_name))
    subm_df.to_csv(subm_score_fp, index=False)

    metrics_df = mean_metrics_dataframe(subm_df, sys_name)
    subm_score_mean = os.path.join(subm_dirpath, "{}_mean_metrics.csv".format(sys_name))
    metrics_df.to_csv(subm_score_mean, index=False)

    if verbose:
        print(subm_df[['trial_id', 'prompt_number', 'correct_tests', 'finds_error_in_incorrect_1',
                       'finds_error_in_incorrect_t', 'code_coverage']])
        print(" ")
        print(f"If you want more information, look at the csvs created here:\n{subm_score_fp}\n{subm_score_mean}\n")
    # if os.path.exists(sys_test_dir) and os.path.isdir(sys_test_dir):
    #    shutil.rmtree(sys_test_dir)
    # Change Working directory back to previous directory
    os.chdir(prev_wd)
    print("VALUE =", value)
    print("Scoring Complete!")
    return value


def code_main(args):
    config_filepath = args.config_filepath
    config_mode = args.config_mode
    key_json_filepath = args.key_filepath
    submission_filepath = args.submission_filepath
    str_current_datetime = args.datetime_for_dir
    temp_working_dir = args.temp_working_dir
    output_dir = args.output_dir
    system_name = args.system_name
    verbose = args.verbose
    print("||| Script: evaluate_submission.py json file")

    if verbose:
        print("Args:")
        print("||| Config File Used: {}".format(config_filepath))
        print("||| Config mode: {}".format(config_mode))
        print("||| Key json Filepath: {}".format(key_json_filepath))
        print("||| Submission Filepath: {}".format(submission_filepath))
        print("||| Temporary Working Directory: {}".format(temp_working_dir))
        print("||| Output Directory: {}".format(output_dir))
        print("||| Datetime Str: {}".format(str_current_datetime))
        print("||| System Name: {}".format(system_name))
    # Show verbosew option
    print("||| Verbose Option: {}. Set verbose to True to print more information".format(verbose))

    evaluate_code_submission(
        str_current_datetime=str_current_datetime,
        key_json_filepath=key_json_filepath,
        submission_json_filepath=submission_filepath,
        temp_test_dir=temp_working_dir,
        output_dir=output_dir,
        system_name=system_name,
        verbose=verbose,
    )


def define_parser():
    """
    Defines accepted CLI syntax and the actions to take for command and args.

    Returns:
        argparse parser

    """

    default_config_filepath = os.environ["GENAI_CODE_CONFIG_PATH"]
    default_config_mode = "Test"

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

    parser = argparse.ArgumentParser(description="Evaluate Test-Code Generating Systems")

    parser.add_argument(
        "-f",
        "--config_filepath",
        help="Location of Configuration file",
        required=False,
        type=str,
        default=default_config_filepath,
    )
    parser.add_argument(
        "-m", "--config_mode", help="Mode of Configuration_file", required=False, type=str,
        default=default_config_mode
    )
    parser.add_argument(
        "-y",
        "--system_name",
        help="System Name",
        required=False,
        type=str,
        default=default_system_name,
    )
    parser.add_argument(
        "-s",
        "--submission_filepath",
        help="Name of submission file with Absolute Path to submission json file. ",
        required=True,
        type=str
    )
    parser.add_argument(
        "-k",
        "--key_filepath",
        help="Absolute path to the key json file.",
        required=True,
        type=str
    )
    datetime_help_str = """ Datetime-string to use for datetime for folders. Put "" to have program make its own'
                            Format as (Y)-(m)-(d)-T(H)-(M)-(S).
                        """
    parser.add_argument(
        "-d", "--datetime_for_dir", help=datetime_help_str, required=False, type=str,
        default=default_datetime_str
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
