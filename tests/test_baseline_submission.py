# import math

import pytest
import os
import sys
import json

sys.path.insert(0, "../genai_code_test")
from genai_code_test.utils.create_baseline_submission import func_create_baseline_submission


class TestWarmupCodeBank(object):

    @pytest.fixture(scope="class")
    def convert_code_bank_to_key_file(self, setup_and_teardown):
        config = setup_and_teardown
        config_mode = "Test"
        root_data_dir = config[config_mode]["root_data_dir"]
        root_output_dir = config[config_mode]["root_output_dir"]
        prob_data_subdir = config[config_mode]["prob_data_subdir"]
        prob_data_dir = os.path.join(root_data_dir, prob_data_subdir)
        output_subdir = config[config_mode]["script_output_subdir"]

        # Conversion 1: Produce the files from the warmup json - these problems are the same as the warmup problems
        prob_json_filepath_dir = os.path.join(prob_data_dir, "code_bank_data.json")
        input_json_filepath_dir = os.path.join(prob_data_dir, "input_data.json")
        prob_output_dir = os.path.join(root_output_dir, output_subdir, "output_create_baseline_submission_file")
        func_create_baseline_submission(prob_json_filepath_dir, input_json_filepath_dir, prob_output_dir)
        return True

    def test_check_code_file_equality(self, setup_and_teardown, convert_code_bank_to_key_file):
        # We are OK if the json code_file elements are in a different order
        config = setup_and_teardown
        config_mode = "Test"
        root_data_dir = config[config_mode]["root_data_dir"]
        root_output_dir = config[config_mode]["root_output_dir"]
        output_subdir = config[config_mode]["script_output_subdir"]
        prob_json_fp = os.path.join(root_data_dir,
                                    "../submissions_test/test_mix_1/baseline_sub_testing.json")
        prob_json_conv_fp = os.path.join(root_output_dir, output_subdir, "output_create_baseline_submission_file",
                                         "nist_baseline_two_test_code_pilot1_smoke_test_problems.json")
        orig_json = open(prob_json_fp, "r")
        orig_data = json.load(orig_json)
        conv_json = open(prob_json_conv_fp, "r")
        conv_data = json.load(conv_json)
        orig_codes = orig_data["code_list"]
        conv_codes = conv_data["code_list"]
        assert len(orig_codes) == len(conv_codes)
        for orig_elem in orig_codes:
            orig_task = orig_elem["trial_id"]
            conv_elem_l = [elem for elem in orig_codes if (elem["trial_id"] == orig_task and int(elem[
                'prompt_number']) == 0)]
            assert len(conv_elem_l) == 1
            # assert orig_elem == conv_elem_l[0]

    def test_check_code_file_equality2(self, setup_and_teardown, convert_code_bank_to_key_file):
        # We are OK if the json code_file elements are in a different order
        config = setup_and_teardown
        config_mode = "Test"
        root_data_dir = config[config_mode]["root_data_dir"]
        root_output_dir = config[config_mode]["root_output_dir"]
        output_subdir = config[config_mode]["script_output_subdir"]
        prob_json_fp = os.path.join(root_data_dir,
                                    "../submissions_test/test_mix_1/baseline_sub_ref_testing.json")
        prob_json_conv_fp = os.path.join(root_output_dir, output_subdir, "output_create_baseline_submission_file",
                                         "nist_baseline_reference_code_pilot1_smoke_test_problems.json")
        orig_json = open(prob_json_fp, "r")
        orig_data = json.load(orig_json)
        conv_json = open(prob_json_conv_fp, "r")
        conv_data = json.load(conv_json)
        orig_codes = orig_data["code_list"]
        conv_codes = conv_data["code_list"]
        assert len(orig_codes) == len(conv_codes)
        for orig_elem in orig_codes:
            orig_task = orig_elem["trial_id"]
            conv_elem_l = [elem for elem in orig_codes if elem["trial_id"] == orig_task and int(elem[
                'prompt_number']) == 0]
            assert len(conv_elem_l) == 1
            # assert orig_elem == conv_elem_l[0]
