import argparse
import json
import os
import configparser
import sys


def func_create_baseline_submission(code_bank_file_path, input_file_path, output_dir):
    """
       This function takes a code_bank_file and an input_file as input values, looks at both files and outputs two
       baseline submission - one is based on the baseline_reference_test_code and the other is based on
       baseline_two_test_code.

       The code_bank_file have the properties of:

        "trial_id"
        "testing_import_statement"
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

        and possibly primary_method_name

       While the input_data have the properties of:

       "trial_id"
       "testing_import_statement"
       "specification"
       "prompt_fixed"

       and possibly primary_method_name

       Args:
           code_bank_file_path: the file path of where the code_bank_data is.
           input_file_path: the file path of where the input_data is.
           output_dir: the directory of where the submissions will be outputted to.

       Returns: Two JSON file that are baseline submission, one is the baseline_reference_test_code and the other is
       the baseline_two_test_code.

       """

    reference_header_data = {}
    reference_all_the_data = []

    twotest_header_data = {}
    twotest_all_the_data = []
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    if os.path.isfile(code_bank_file_path) and os.path.isfile(input_file_path) == False:
        print("Either the code_bank or input_file does not exist, recheck path files and try again!")

    else:
        code_bank_jf = open(code_bank_file_path, "r")
        code_bank_data = json.load(code_bank_jf)

        input_file_jf = open(input_file_path, "r")
        input_file_data = json.load(input_file_jf)

        version = input_file_data["version"]
        name = code_bank_data["name"]

        input_file_elements = input_file_data["code_list"]
        code_bank_elements = code_bank_data["code_list"]

        for input_data in input_file_elements:
            trial_id = input_data["trial_id"]
            prompt_number = "0"
            custom_prompt_number = "1"
            prompt = input_data["prompt_fixed"]

            try:
                primary_method_name = input_data["primary_method_name"]
            except KeyError:
                print("No primary_method_name file")
                primary_method_name = "*"

            code_data_list = [x for x in code_bank_elements if x["trial_id"] == input_data["trial_id"]]
            code_data = code_data_list[0]

            # making reference baseline first
            reference_result = name[10:]
            modified_text_reference = reference_result.replace(" ", "_").lower()
            reference_new_name = "NIST Baseline Reference Code Submission " + reference_result + " Fixed Track"
            reference_system = "nist_baseline_reference_code"
            reference_title = "nist_baseline_reference_code_" + modified_text_reference + ".json"

            reference_test_output = code_data["baseline_reference_test_code"]
            reference_test_code = code_data["baseline_reference_test_code"]

            reference_header_data["name"] = reference_new_name
            reference_header_data["version"] = version
            reference_header_data["system"] = reference_system
            reference_header_data["code_list"] = []

            # Assemble the structure
            reference_metadata = {
                "trial_id": trial_id,
                "prompt_number": prompt_number,
                "prompt": prompt,
                "primary_method_name": primary_method_name,
                "test_output": reference_test_output,
                "test_code": reference_test_code,
            }

            # Assemble the custom structure
            reference_metadata_custom = {
                "trial_id": trial_id,
                "prompt_number": custom_prompt_number,
                "prompt": prompt,
                "primary_method_name": primary_method_name,
                "test_output": reference_test_output,
                "test_code": reference_test_code,
            }

            reference_header_data["name"] = reference_new_name
            reference_header_data["version"] = version
            reference_header_data["system"] = reference_system
            reference_all_the_data.append(reference_metadata)
            reference_all_the_data.append(reference_metadata_custom)

            reference_header_data["code_list"] = reference_all_the_data
            reference_output_file = os.path.join(output_dir, reference_title)
            with open(reference_output_file, "w") as reference_fp:
                json.dump(reference_header_data, reference_fp, indent=2)

            # making two test baseline now
            twotest_result = name[10:]
            modified_text = twotest_result.replace(" ", "_").lower()
            twotest_new_name = "NIST Baseline Two Test Code Submission " + twotest_result + " Fixed Track"
            twotest_system = "nist_baseline_two_test_code"
            twotest_title = "nist_baseline_two_test_code_" + modified_text + ".json"

            twotest_test_output = code_data["baseline_two_test_code"]
            twotest_test_code = code_data["baseline_two_test_code"]

            twotest_header_data["name"] = twotest_new_name
            twotest_header_data["version"] = version
            twotest_header_data["system"] = twotest_system
            twotest_header_data["code_list"] = []

            # Assemble the structure
            twotest_metadata = {
                "trial_id": trial_id,
                "prompt_number": prompt_number,
                "prompt": prompt,
                "primary_method_name": primary_method_name,
                "test_output": twotest_test_output,
                "test_code": twotest_test_code,
            }

            # Assemble the custom structure
            twotest_metadata_custom = {
                "trial_id": trial_id,
                "prompt_number": custom_prompt_number,
                "prompt": prompt,
                "primary_method_name": primary_method_name,
                "test_output": twotest_test_output,
                "test_code": twotest_test_code,
            }

            twotest_header_data["name"] = twotest_new_name
            twotest_header_data["version"] = version
            twotest_header_data["system"] = twotest_system
            twotest_all_the_data.append(twotest_metadata)
            twotest_all_the_data.append(twotest_metadata_custom)

            twotest_header_data["code_list"] = twotest_all_the_data
            twotest_output_file = os.path.join(output_dir, twotest_title)
            with open(twotest_output_file, "w") as twotest_fp:
                json.dump(twotest_header_data, twotest_fp, indent=2)


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
        "-c",
        "--code_bank_file",
        help="Absolute Path of code bank file to use for a submission reference.",
        required=False,
        type=str,
    )
    parser.add_argument(
        "-i",
        "--input_file",
        help="Absolute Path of input file to use for a submission reference.",
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
    code_bank_file = args.code_bank_file
    input_file = args.input_file
    output_dir = args.output_dir
    verbose = args.verbose
    print("||| Script: create_code_files_from_json_input")

    print("Args:")
    print("||| Config File Used: {}".format(config_filepath))
    print("||| Config mode: {}".format(config_mode))
    print("||| Code Bank File Path: {}".format(code_bank_file))
    print("||| Input File Path: {}".format(input_file))
    print("||| Output Directory Path: {}".format(output_dir))
    print("||| Verbose Option: {}. Set verbose to True to print more information".format(verbose))

    func_create_baseline_submission(code_bank_file, input_file, output_dir)


def main():
    parser = define_parser()
    args = parser.parse_args()
    if hasattr(args, "func") and args.func is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
