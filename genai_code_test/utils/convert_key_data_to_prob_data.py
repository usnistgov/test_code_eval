import argparse
import json
import os
import configparser
import sys
import re


def making_fixed_prompt(specification, primary_method_name):
    """
    Generates our fixed prompt for a particular trial with a given specification.

    Args:
        specification: the text specification of the problem
        primary_method_name: the primary method name of the problem for a trial

    Returns: (str) A string of the fixed prompt constructed.

    """
    intro_string = ("We have python code that implements the following "
                    "specification.\n\nSpecification:")

    spec_string = f"\n\n{specification}\n\n"
    code_string = ""
    instruction_string = (
        f"Please write python pytest test code that comprehensively "
        f"tests the code for method {primary_method_name} "
        f"to determine if the code satisfies the specification or not. When writing tests:\n"
        f"* write a comprehensive test suite,\n"
        f"* test edge cases,\n"
        f"* only generate correct tests, and\n"
        f"* include tests for TypeError cases.\n\n"
        f"Please write '###|=-=-=beginning of tests=-=-=|' before the tests. "
        f"Write '###|=-=-=end of tests=-=-=|' immediately after the tests. "
        f"Import any needed packages, including pytest. Import the code being tested by adding the line "
        f"`from genai_code_file import {primary_method_name}` the line after '###|=-=-=beginning of tests=-=-=|'. "
        f"Do not provide an implementation of the method {primary_method_name} with the tests.")
    the_prompt_fixed = intro_string + spec_string + code_string + instruction_string

    return the_prompt_fixed


def func_convert_key_data_to_prob_data(input_dir, output_dir):
    """
    This function takes a directory as an input value, looks at the JSON key file or files within the directory and
    outputs a JSON input file. This input file that is created will be the file participants will being using
    during the pilot study.

    These key files have the properties of:

    "trial_id"
    "testing_import_statement"
    "source"
    "source_text"
    "category"
    "specification"
    "code_correct":
    "code_incorrect_1"
    "code_incorrect_t"

    and possibly primary_method_name

    While the problem files have the properties of:

    "trial_id"
    "testing_import_statement"
    "specification"
    "prompt_fixed"

    and possibly primary_method_name

    Args:
        input_dir: the directory where the JSON key file is.
        output_dir: the directory where the JSON input file will be.

    Returns: The input JSON file.

    """
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    json_list = []
    num = 0

    for file in os.listdir(input_dir):
        if file.endswith(".json"):
            json_list.append(file)

    for i in json_list:
        all_the_data = []
        header_data = {}

        problem_directory = os.path.join(input_dir, i)
        jf = open(problem_directory, "r")
        input_data = json.load(jf)
        elements = input_data["code_list"]

        name = input_data["name"]
        result = name[15:]
        new_name = "Problem Inputs for " + result
        version = input_data["version"]
        eval_version = input_data["Evaluation_Version"]

        for e in elements:
            trial_id = e["trial_id"]

            try:
                primary_method_name = e["primary_method_name"]
            except KeyError:
                print("No primary_method_name file")
                primary_method_name = "*"

            pattern = r'\bdef\s+(\w+)\('
            method_names = re.findall(pattern, e['code_correct'])

            if method_names:
                testing_import_statement = f"from genai_code_file import {",".join(method_names)}"
            else:
                testing_import_statement = ""

            name = trial_id[6:]
            specification = e["specification"]

            prompt_fixed = making_fixed_prompt(specification, primary_method_name)

            header_data["name"] = new_name
            header_data["version"] = version
            header_data["Evaluation_Version"] = eval_version
            header_data["code_list"] = []

            # Assemble the structure
            metadata = {
                "trial_id": trial_id,
                "testing_import_statement": testing_import_statement,
                "primary_method_name": primary_method_name,
                "specification": specification,
                "prompt_fixed": prompt_fixed,
            }

            header_data["name"] = new_name
            header_data["version"] = version
            header_data["Evaluation_Version"] = eval_version
            all_the_data.append(metadata)
            num = num + 25

        header_data["code_list"] = all_the_data
        output_fname = i.replace("key", "input")
        output_file = os.path.join(output_dir, output_fname)
        with open(output_file, "w") as fp:
            json.dump(header_data, fp, indent=2)


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
        required=False,
        type=str,
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        help="Absolute path to the output directory where converted folders should be created. "
             "May overwrite past output.",
        required=False,
        type=str,
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

    func_convert_key_data_to_prob_data(input_dir, output_dir)


def main():
    parser = define_parser()
    args = parser.parse_args()
    if hasattr(args, "func") and args.func is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
