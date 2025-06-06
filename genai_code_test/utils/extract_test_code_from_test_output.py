import json
import pandas as pd
import argparse
import configparser
import os
import sys

# from mpmath import isint


def extract_test_code_from_prompt_output_pri(output_str, trial_id):
    """
    Extract the test code statements from our AI prompt output given the structure of our fixed prompt. This
    Leverages that our prompts start with  "###|=-=-=beginning of tests=-=-=|" before the code and
    "###|=-=-=end of tests=-=-=|" at the end of the code. Prompt output not containing this will not be
    converted by this method and will rely on the extract_test_code_from_prompt_output_sec() method to extract
    the prompt.

    Args:
        output_str: The string containing the entirety of the AI-generated system output, which includes all the
            test code.
        trial_id: The trial id of the trial.

    Returns: a string with as the converted test code that can be run in pytest or "" if the test code could not
        be extracted.

    """
    code_start = 0
    code_end = len(output_str)
    test_start_str = "###|=-=-=beginning of tests=-=-=|"
    test_end_str = "###|=-=-=end of tests=-=-=|"
    try:
        start_loc = output_str.index(test_start_str)
        code_start = start_loc + len(test_start_str)
    except IndexError as errex:
        print(errex)
        print("ERROR: Test-Starting String {} missing for Trial {}".format(test_start_str, trial_id))
        return ""
    except ValueError as errex:
        print(errex)
        print("ERROR: Test-Starting String {} missing for Trial {}".format(test_start_str, trial_id))
        return ""
    try:
        end_loc = output_str.index(test_end_str)
        code_end = end_loc
    except IndexError as errex:
        print(errex)
        print("ERROR: Test Ending String {} missing or "
              "before start string for Trial {}".format(test_end_str, trial_id))
        return ""
    except ValueError as errex:
        print(errex)
        print("ERROR: Test Ending String {} missing or "
              "before start string for Trial {}".format(test_end_str, trial_id))
        return ""
    if end_loc <= start_loc:
        print(
            "ERROR: Test End String {} Before Test Start String {} for Trial {}".format(
                test_end_str,
                test_start_str,
                trial_id))
        return ""
    output_code_str = output_str[code_start:code_end].strip('\n\r')
    output_code_str = output_code_str.replace("```", "#```")
    return output_code_str


def extract_test_code_from_prompt_output_sec(output_str, trial_id):
    """
    Extract the test code statements from our AI prompt output given the structure of our fixed prompt when
    the primary extractor fails. We also realize that some systems encapsulate their code
    in ```python <code> ```, so we use this as a secondary catch if our instructions are not followed.

    Args:
        output_str: The string containing the entirety of the AI-generated system output, which includes all the
            test code.
        trial_id: The trial id of the trial.

    Returns: a string with as the converted test code that can be run in pytest or "" if the test code could not
        be extracted.

    """

    code_start = 0
    code_end = len(output_str)
    test_start_str = "```python"
    test_end_str = "```"
    try:
        start_loc = output_str.rindex(test_start_str)
        code_start = start_loc + len(test_start_str)
    except IndexError as errex:
        print(errex)
        print("ERROR: Secondary Test-Starting String {} missing for Trial {}".format(test_start_str, trial_id))
        return ""
    except ValueError as errex:
        print(errex)
        print("ERROR: Secondary Test-Starting String {} missing for Trial {}".format(test_start_str, trial_id))
        return ""
    output_post_start_str = output_str[code_start:]
    try:
        end_loc = output_post_start_str.index(test_end_str)
        code_end = end_loc
    except IndexError as errex:
        print(errex)
        print("ERROR: Secondary Test Ending String {} missing or "
              "before start string for Trial {}".format(test_end_str, trial_id))
        return ""
    except ValueError as errex:
        print(errex)
        print("ERROR: Secondary Test Ending String {} missing or "
              "before start string for Trial {}".format(test_end_str, trial_id))
        return ""
    output_code_str = output_post_start_str[:code_end].strip('\n\r')
    output_code_str = output_code_str.replace("```", "#```")
    return output_code_str


def convert_submission(ai_json_fp, output_fp):
    """
    Main method to extract test code from AI-generated prompts. This code takes a json submission output produced by
    our LLM-querying code that includes the entirety of the AI-generated output in test_output but is missing the
    extracted test_code field. This method extracts the test code from the test_ouptut and provides the test_code. Then
    it creates a valid submission json file with the test code.

    Args:
        ai_json_fp: absolute file path to the AI-submission json file without the test_code
        output_fp:  absolute file path to write the output json submission file to.

    Returns:

    """
    ai_jf = open(ai_json_fp, "r")
    ai_data = json.load(ai_jf)
    ai_elements = ai_data["code_list"]
    code_dict = {
        "name": ai_data["name"],
        "version": ai_data["version"],
        "system": ai_data["system"],
        "code_list": [],
    }
    for e in ai_elements:
        e_code_file = e.copy()
        output_str = e_code_file["test_output"]
        trial_id = e["trial_id"]
        test_import_statement = "from genai_code_file import *"
        if "testing_import_statement" in e:
            test_import_statement = e['testing_import_statement']
        output_code_str = extract_test_code_from_prompt_output_pri(output_str, trial_id)
        if output_code_str == "":
            output_code_str = extract_test_code_from_prompt_output_sec(output_str, trial_id)
        # Now we augment it with our import line only if we don't see it
        try:
            output_str.index("from genai_code_file import")
            test_code_str = output_code_str
        except IndexError:
            test_code_str = test_import_statement + "\n\n" + output_code_str
        except ValueError:
            test_code_str = test_import_statement + "\n\n" + output_code_str
        # For our test code extraction, convert any integer prompt number to a string
        # if isinstance(e_code_file["prompt_number"], int):
        #     e_code_file["prompt_number"] = str(e_code_file["prompt_number"])
        e_code_file["test_output"] = output_str
        e_code_file["test_code"] = test_code_str
        code_dict["code_list"].append(e_code_file)
    if not os.path.isdir(os.path.dirname(output_fp)):
        os.makedirs(os.path.dirname(output_fp))
    with open(output_fp, "w") as fp:
        json.dump(code_dict, fp, indent=2)


def code_main(args):
    input_filepath = args.input_filepath
    output_filepath = args.output_filepath
    verbose = args.verbose
    print("||| Script: create_test_code_from_test_output.py")

    print("Args:")
    print("||| Input Submission Filepath: {}".format(input_filepath))
    print("||| Output Converted Filepath: {}".format(output_filepath))
    print("||| Verbose Option: {}. Set verbose to True to print more information".format(verbose))

    convert_submission(input_filepath, output_filepath)


def define_parser():
    """
    Defines accepted CLI syntax and the actions to take for command and args.

    Returns:
        argparse parser

    """

    default_config_filepath = os.environ["GENAI_CODE_CONFIG_PATH"]

    # Now extract the arguments from the config file
    try:
        config = configparser.ConfigParser()
        with open(default_config_filepath) as configfile:
            config.read_file(configfile)
    except ImportError:
        sys.exit("Cannot open config file: " + default_config_filepath)

    parser = argparse.ArgumentParser(description="Evaluate Test-Code Generating Systems")

    parser.add_argument(
        "-i",
        "--input_filepath",
        help="Filepath of the input submission file. ",
        required=True,
        type=str
    )

    parser.add_argument(
        "-o",
        "--output_filepath",
        help="Absolute path to the output json filepath of the converted submission file.",
        required=True,
        type=str
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
