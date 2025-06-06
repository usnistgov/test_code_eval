#! /usr/bin/env python
import argparse
import glob
import json
import os
import configparser
import sys


def func_create_json_file_from_code_files(input_dir, output_dir):
    """
    This function takes a problem folder and the metadata JSON file associated with the problem folder as an input and
    creates an output which is a new JSON file that contains all the information from the folders and metadata.

    These are the properties of the output JSON file:
    "trial_id"
    "testing_import_statement"
    "primary_method_name"
    "source"
    "source_text"
    "lines_per_method"
    "num_methods"
    "imports_used"
    "category"
    "specification"
    "code_correct"
    "code_incorrect_1"
    "code_incorrect_t"
    "baseline_reference_test_code"
    "baseline_two_test_code"


    Args:
        input_dir: the directory where the folder for each problem and the metadata JSON file are.
        output_dir: the directory where the new JSON file will be located. This JSON contains the information from
        the problem folder and metadata file.

    Returns: a JSON file. The naming convention is the name, version and converted attached by underscores
    so for example - code_bank_pilot_smoke_test_problems_0d91_converted.json

    """
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    is_value = True
    file_number = 1

    metadatafile = glob.glob(f"{input_dir}/**/metadata.json", recursive=True)

    for metadata_file in metadatafile:
        with open(metadata_file) as file:
            text = json.load(file)

        name = text['name']
        version = text['version']
        eval_version = text['Evaluation_Version']
        problems = text['code_list']

        code_dict = {"name": name, "version": version, "Evaluation_Version": eval_version, "code_list": []}

        for prob in problems:
            task_name = prob['trial_id']
            if not task_name:
                is_value = False

            problem_folders = glob.glob(f"{input_dir}/**/*", recursive=True)

            for folder in problem_folders:
                folder_path = os.path.join(input_dir, folder)
                if os.path.isdir(folder_path) and task_name in folder:
                    task_directory = folder_path

            # Getting the specific file from each problem directory that we want
            specification_fp = os.path.join(task_directory, f"{task_name}_specification.txt")
            code_correct_fp = os.path.join(task_directory, f"{task_name}_correct.py")
            code_incorrect_1_fp = os.path.join(task_directory, f"{task_name}_incorrect_1.py")
            code_baseline_reference_test_code_fp = os.path.join(task_directory,
                                                                f"{task_name}_baseline_reference_test_code.py")
            code_baseline_two_test_code_fp = os.path.join(task_directory,
                                                          f"{task_name}_baseline_two_test_code.py")
            try:
                code_incorrect_t_fp = os.path.join(task_directory, f"{task_name}_incorrect_t.py")
            except code_incorrect_t_fp.DoesNotExist:
                print("No code_incorrect_t file")
                continue

            testing_import_statement = prob["testing_import_statement"]
            if not testing_import_statement:
                is_value = False

            source = prob["source"]
            if not source:
                is_value = False

            source_text = prob["source_text"]

            lines_per_method = prob["lines_per_method"]
            if not lines_per_method:
                is_value = False

            num_methods = prob["num_methods"]
            if not num_methods:
                is_value = False

            imports_used = prob["imports_used"]
            if not imports_used:
                is_value = False

            category = prob["category"]
            if not category:
                is_value = False

            try:
                primary_method_name = prob["primary_method_name"]
            except KeyError:
                print("No primary_method_name file")
                primary_method_name = "*"

            text_specification = ""
            with open(specification_fp) as file_text_specification:
                text_specification = file_text_specification.read()
            if not text_specification:
                is_value = False

            text_code = ""
            with open(code_correct_fp) as file_text_code:
                text_code = file_text_code.read()
            if not text_code:
                is_value = False

            text_code_incorrect_1 = ""
            with open(code_incorrect_1_fp) as file_text_code_incorrect_1:
                text_code_incorrect_1 = file_text_code_incorrect_1.read()
            if not text_code_incorrect_1:
                is_value = False

            try:
                text_code_incorrect_t = ""
                with open(code_incorrect_t_fp) as file_text_code_incorrect_t:
                    text_code_incorrect_t = file_text_code_incorrect_t.read()
                if not text_code_incorrect_t:
                    is_value = False
            except OSError:
                print("No code_incorrect_t file")
                text_code_incorrect_t = "No code_incorrect_t"

            text_code_baseline_reference_test_code = ""
            with open(code_baseline_reference_test_code_fp) as file_text_code_baseline_reference_test_code:
                text_code_baseline_reference_test_code = file_text_code_baseline_reference_test_code.read()
            if not text_code_baseline_reference_test_code:
                is_value = False

            text_code_baseline_two_test_code = ""
            with open(code_baseline_two_test_code_fp) as file_text_code_baseline_two_test_code:
                text_code_baseline_two_test_code = file_text_code_baseline_two_test_code.read()
            if not text_code_baseline_two_test_code:
                is_value = False

            e_code_file = {
                "trial_id": task_name,
                "testing_import_statement": testing_import_statement,
                "source": source,
                "source_text": source_text,
                "lines_per_method": lines_per_method,
                "num_methods": num_methods,
                "imports_used": imports_used,
                "category": category,
                "primary_method_name": primary_method_name,
                "specification": text_specification,
                "code_correct": text_code,
                "code_incorrect_1": text_code_incorrect_1,
                "code_incorrect_t": text_code_incorrect_t,
                "baseline_reference_test_code": text_code_baseline_reference_test_code,
                "baseline_two_test_code": text_code_baseline_two_test_code
            }
            code_dict["code_list"].append(e_code_file)

        new_name = name.replace(" ", "_")
        new_version = version.replace(".", "d")
        output_file = os.path.join(output_dir, f"{new_name}_{new_version}_converted.json").lower()
        with open(output_file, "w") as fp:
            json.dump(code_dict, fp, indent=2)

        file_number = file_number + 1

    return is_value


def define_parser():
    """
    Defines accepted CLI syntax and the actions to take for command and args.

    Returns:
        argparse parser

    """

    default_config_filepath = os.environ["GENAI_CODE_CONFIG_PATH"]
    default_config_mode = "Pilot1Evaluator"

    try:
        config = configparser.ConfigParser()
        with open(default_config_filepath) as configfile:
            config.read_file(configfile)
    except ImportError:
        sys.exit("Cannot open config file: " + default_config_filepath)

    # root_data_dir = config[default_config_mode]["root_data_dir"]
    # root_output_dir = config[default_config_mode]["root_output_dir"]
    # prob_data_subdir = config[default_config_mode]["prob_data_subdir"]
    # script_output_subdir = config[default_config_mode]["script_output_subdir"]
    # prob_data_dir = os.path.join(root_data_dir, prob_data_subdir)
    # script_output_dir = os.path.join(root_output_dir, script_output_subdir)

    # default_input_dir = os.path.join(prob_data_dir)
    # default_output_dir = os.path.join(script_output_dir, "json_file_from_code_files_testing")

    parser = argparse.ArgumentParser(description="Create Code Files from json Input")

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
        "-i",
        "--input_dir",
        help="Absolute Path of input directory of json files to convert.",
        required=False,
        type=str,
        # default=default_input_dir,
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        help="Absolute path to the output directory where converted folders should be created. "
             "May overwrite past output.",
        required=False,
        type=str,
        # default=default_output_dir,
    )
    parser.add_argument(
        "-v", "--verbose", help="Enable Verbose output", required=False, action="store_true", default=False
    )

    # This tells the code to automatically execute this function
    parser.set_defaults(func=code_main)
    return parser


def code_main(args):
    config_filepath = args.config_filepath
    config_mode = args.config_mode
    input_dir = args.input_dir
    output_dir = args.output_dir
    verbose = args.verbose
    print("||| Script: create_code_files_from_json_input")

    print("Args:")
    print("||| Config File Used: {}".format(config_filepath))
    print("||| Config mode: {}".format(config_mode))
    print("||| Input Directory Path: {}".format(input_dir))
    print("||| Output Directory Path: {}".format(output_dir))
    print("||| Verbose Option: {}. Set verbose to True to print more information".format(verbose))

    func_create_json_file_from_code_files(input_dir, output_dir)


def main():
    parser = define_parser()
    args = parser.parse_args()
    if hasattr(args, "func") and args.func is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
