#! /usr/bin/env python
import os
import json
import configparser
import sys
import argparse


def func_create_code_files_from_json(prob_data_dir, output_dir):
    """
    This function takes a directory as an input value, looks at the problem JSON file within a directory and outputs a
    folder what contains a folder for each problem in the JSON file and a metadata file. Each problem folder is
    labeled by its trial_id and contains a file for the baseline reference code, baseline two test code,
    the incorrect code, the incorrect t, the correct code and the specification. The metadata JSON file consists of
    all the metadata from the problems.

    The metadata properties are:
    "trial_id"
    "testing_import_statement"
    "source"
    "source_text"
    "lines_per_method"
    "num_methods"
    "imports_used"
    "category"


    Args:
        prob_data_dir: the directory where the problem JSON file is.
        output_dir: the directory where the folder and metadata JSON file will be.

    Returns: a folder for each problem and a metadata JSON file which contains data for all the problems.

    """
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    is_value = True
    json_file = []
    all_the_data = []
    header_data = {}

    for file in os.listdir(prob_data_dir):
        if file.endswith(".json"):
            json_file.append(file)

    for i in json_file:
        problem_directory = os.path.join(prob_data_dir, i)
        jf = open(problem_directory, "r")
        input_data = json.load(jf)
        elements = input_data["code_list"]

        name = input_data["name"]
        version = input_data["version"]
        eval_version = input_data["Evaluation_Version"]

        json_basename = os.path.splitext(os.path.basename(problem_directory))[0]
        json_output_dir = os.path.join(output_dir, json_basename)

        for e in elements:
            suboutput_dir = os.path.join(json_output_dir, e["trial_id"])
            if not os.path.isdir(suboutput_dir):
                os.makedirs(suboutput_dir)

            task_name = e["trial_id"]
            if not task_name:
                is_value = False

            testing_import_statement = ""
            if "testing_import_statement" in e:
                testing_import_statement = e["testing_import_statement"]
                if not testing_import_statement:
                    is_value = False

            md_source = ""
            if "source" in e:
                md_source = e["source"]
                if not md_source:
                    is_value = False

            md_source_text = ""
            if "source_text" in e:
                md_source_text = e["source_text"]

            md_lines_per_method = ""
            if "lines_per_method" in e:
                md_lines_per_method = e["lines_per_method"]
                if not md_lines_per_method:
                    is_value = False

            md_num_methods = ""
            if "num_methods" in e:
                md_num_methods = e["num_methods"]
                if not md_num_methods:
                    is_value = False

            md_imports_used = ""
            if "imports_used" in e:
                md_imports_used = e["imports_used"]
                if not md_imports_used:
                    is_value = False

            category = ""
            if "category" in e:
                category = e["category"]
                if not category:
                    is_value = False

            try:
                primary_method_name = e["primary_method_name"]
            except KeyError:
                print("No primary_method_name file")
                primary_method_name = "*"

            if "specification" in e:
                text_specification = e["specification"]
                specification_fp = os.path.join(suboutput_dir, task_name + "_specification.txt")
                with open(specification_fp, "w") as text_file:
                    text_file.write(text_specification)
                    if not text_specification:
                        is_value = False

            if "code_correct" in e:
                text_code_correct = e["code_correct"]
                correct_code_fp = os.path.join(suboutput_dir, task_name + "_correct.py")
                with open(correct_code_fp, "w") as text_file:
                    text_file.write(text_code_correct)
                    if not text_code_correct:
                        is_value = False

            if "code_incorrect_1" in e:
                text_code_incorrect_1 = e["code_incorrect_1"]
                incorrect_1_code_fp = os.path.join(suboutput_dir, task_name + "_incorrect_1.py")
                with open(incorrect_1_code_fp, "w") as text_file:
                    text_file.write(text_code_incorrect_1)
                    if not text_code_incorrect_1:
                        is_value = False

            try:
                if "code_incorrect_t" in e:
                    text_code_incorrect_t = e["code_incorrect_t"]
                    incorrect_t_code_fp = os.path.join(suboutput_dir, task_name + "_incorrect_t.py")
                    with open(incorrect_t_code_fp, "w") as text_file:
                        text_file.write(text_code_incorrect_t)
                        if not text_code_incorrect_t:
                            is_value = False
            except text_code_incorrect_t.DoesNotExist:
                print("No code_incorrect_t file")
                continue

            if "baseline_reference_test_code" in e:
                baseline_reference_test_code = e["baseline_reference_test_code"]
                baseline_reference_test_code_fp = os.path.join(suboutput_dir, task_name +
                                                               "_baseline_reference_test_code.py")
                with open(baseline_reference_test_code_fp, "w") as text_file:
                    text_file.write(baseline_reference_test_code)
                    if not baseline_reference_test_code:
                        is_value = False

            if "baseline_two_test_code" in e:
                baseline_two_test_code = e["baseline_two_test_code"]
                baseline_two_test_code_fp = os.path.join(suboutput_dir, task_name + "_baseline_two_test_code.py")
                with open(baseline_two_test_code_fp, "w") as text_file:
                    text_file.write(baseline_two_test_code)
                    if not baseline_two_test_code:
                        is_value = False

            if "prompt" in e:
                prompt_text = e["prompt"]
                prompt_text_fp = os.path.join(suboutput_dir, task_name + "_prompt.txt")
                with open(prompt_text_fp, "w") as text_file:
                    text_file.write(prompt_text)
                    if not prompt_text:
                        is_value = False

            if "prompt_fixed" in e:
                prompt_fixed_text = e["prompt_fixed"]
                prompt_fixed_text_fp = os.path.join(suboutput_dir, task_name + "_prompt_fixed.txt")
                with open(prompt_fixed_text_fp, "w") as text_file:
                    text_file.write(prompt_fixed_text)
                    if not prompt_fixed_text:
                        is_value = False

            header_data["name"] = name
            header_data["version"] = version
            header_data["Evaluation_Version"] = eval_version
            header_data["code_list"] = []

            metadata = {

                "trial_id": task_name,
                "testing_import_statement": testing_import_statement,
                "source": md_source,
                "source_text": md_source_text,
                "lines_per_method": md_lines_per_method,
                "num_methods": md_num_methods,
                "imports_used": md_imports_used,
                "category": category,
                "primary_method_name": primary_method_name
            }

            header_data["name"] = name
            header_data["version"] = version
            header_data["Evaluation_Version"] = eval_version
            all_the_data.append(metadata)

        header_data["code_list"] = all_the_data
        output_file = os.path.join(json_output_dir, "metadata.json")
        with open(output_file, "w") as fp:
            json.dump(header_data, fp, indent=2)
        all_the_data = []

    if is_value:
        return True
    else:
        return False


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
        required=True,
        type=str
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        help="Absolute path to the output directory where converted folders should be created. "
             "May overwrite past output.",
        required=True,
        type=str
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

    func_create_code_files_from_json(input_dir, output_dir)


def main():
    parser = define_parser()
    args = parser.parse_args()
    if hasattr(args, "func") and args.func is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
