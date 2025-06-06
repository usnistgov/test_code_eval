import os
import json
import pytest
import sys

sys.path.insert(0, "../genai_code_test")
from genai_code_test.utils.extract_test_code_from_test_output import convert_submission


@pytest.fixture
def extraction_case_1(setup_and_teardown):
    config = setup_and_teardown
    config_mode = "Test"
    root_data_dir = config[config_mode]["root_data_dir"]
    root_output_dir = config[config_mode]["root_output_dir"]
    orig_data_dir = os.path.join(root_data_dir, "extraction_of_tests")
    output_subdir = config[config_mode]["script_output_subdir"]
    output_dir = os.path.join(root_output_dir, output_subdir)

    # Extraction 1:
    input_submission_fp = os.path.join(orig_data_dir, "test_output_1.json")
    output_fp = os.path.join(output_dir, "test_output_1_extracted_tests.json")
    convert_submission(input_submission_fp, output_fp)
    return True


@pytest.fixture
def extraction_case_2(setup_and_teardown):
    config = setup_and_teardown
    config_mode = "Test"
    root_data_dir = config[config_mode]["root_data_dir"]
    root_output_dir = config[config_mode]["root_output_dir"]
    orig_data_dir = os.path.join(root_data_dir, "extraction_of_tests")
    output_subdir = config[config_mode]["script_output_subdir"]
    output_dir = os.path.join(root_output_dir, output_subdir)

    # Extraction 1:
    input_submission_fp = os.path.join(orig_data_dir, "test_output_2.json")
    output_fp = os.path.join(output_dir, "test_output_2_extracted_tests.json")
    convert_submission(input_submission_fp, output_fp)
    return True


def test_extraction_of_tests_1(setup_and_teardown, extraction_case_1):
    config = setup_and_teardown
    config_mode = "Test"
    root_data_dir = config[config_mode]["root_data_dir"]
    root_output_dir = config[config_mode]["root_output_dir"]
    gt_data_dir = os.path.join(root_data_dir, "extraction_of_tests")
    conv_subdir = config[config_mode]["script_output_subdir"]
    conv_dir = os.path.join(root_output_dir, conv_subdir)

    gt_fp = os.path.join(gt_data_dir, "test_output_1_extracted.json")
    conv_fp = os.path.join(conv_dir, "test_output_1_extracted_tests.json")

    gt_json = open(gt_fp, "r")
    gt_data = json.load(gt_json)
    conv_json = open(conv_fp, "r")
    conv_data = json.load(conv_json)

    gt_codes = gt_data["code_list"]
    conv_codes = conv_data["code_list"]
    assert len(gt_codes) == len(conv_codes)
    for gt_elem in gt_codes:
        gt_task = gt_elem["trial_id"]
        conv_elem_l = [elem for elem in gt_codes if elem["trial_id"] == gt_task]
        assert len(conv_elem_l) == 1
        assert gt_elem["test_code"] == conv_elem_l[0]["test_code"]


def test_extraction_of_tests_2(setup_and_teardown, extraction_case_2):
    config = setup_and_teardown
    config_mode = "Test"
    root_data_dir = config[config_mode]["root_data_dir"]
    root_output_dir = config[config_mode]["root_output_dir"]
    gt_data_dir = os.path.join(root_data_dir, "extraction_of_tests")
    conv_subdir = config[config_mode]["script_output_subdir"]
    conv_dir = os.path.join(root_output_dir, conv_subdir)

    gt_fp = os.path.join(gt_data_dir, "test_output_2_extracted.json")
    conv_fp = os.path.join(conv_dir, "test_output_2_extracted_tests.json")

    gt_json = open(gt_fp, "r")
    gt_data = json.load(gt_json)
    conv_json = open(conv_fp, "r")
    conv_data = json.load(conv_json)

    gt_codes = gt_data["code_list"]
    conv_codes = conv_data["code_list"]
    assert len(gt_codes) == len(conv_codes)
    for gt_elem in gt_codes:
        gt_task = gt_elem["trial_id"]
        conv_elem_l = [elem for elem in gt_codes if elem["trial_id"] == gt_task]
        assert len(conv_elem_l) == 1
        assert gt_elem["test_code"] == conv_elem_l[0]["test_code"]
