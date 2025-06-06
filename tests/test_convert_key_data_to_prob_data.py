import pytest
import os
import sys
import json

sys.path.insert(0, "../genai_code_test")
from genai_code_test.utils.convert_key_data_to_prob_data import func_convert_key_data_to_prob_data


class TestWarmupCodeBank(object):

    @pytest.fixture
    def convert_key_data_to_prob_data(self, setup_and_teardown):
        config = setup_and_teardown
        config_mode = "Test"
        root_data_dir = config[config_mode]["root_data_dir"]
        root_output_dir = config[config_mode]["root_output_dir"]
        prob_data_subdir = config[config_mode]["prob_data_subdir"]
        prob_data_dir = os.path.join(root_data_dir, prob_data_subdir)
        output_subdir = config[config_mode]["script_output_subdir"]

        # Conversion 1: Produce the files from the warmup json - these problems are the same as the warmup problems
        prob_json_filepath_dir = os.path.join(prob_data_dir, "testing_convert_key_data_to_prob_data")
        prob_output_dir = os.path.join(root_output_dir, output_subdir, "output_convert_key_data_to_prob_data")
        func_convert_key_data_to_prob_data(prob_json_filepath_dir, prob_output_dir)
        return True

    def test_check_code_file_equality(self, setup_and_teardown, convert_key_data_to_prob_data):
        # We are OK if the json code_file elements are in a different order
        config = setup_and_teardown
        config_mode = "Test"
        root_data_dir = config[config_mode]["root_data_dir"]
        root_output_dir = config[config_mode]["root_output_dir"]
        output_subdir = config[config_mode]["script_output_subdir"]
        prob_json_fp = os.path.join(root_data_dir,
                                    "practice_problem_data/prob_data_from_key_data_output.json")
        prob_json_conv_fp = os.path.join(root_output_dir, output_subdir, "output_convert_key_data_to_prob_data",
                                         "warmup.json")
        orig_json = open(prob_json_fp, "r")
        orig_data = json.load(orig_json)
        conv_json = open(prob_json_conv_fp, "r")
        conv_data = json.load(conv_json)
        orig_codes = orig_data["code_list"]
        conv_codes = conv_data["code_list"]
        assert len(orig_codes) == len(conv_codes)
        for orig_elem in orig_codes:
            orig_task = orig_elem["trial_id"]
            conv_elem_l = [elem for elem in orig_codes if elem["trial_id"] == orig_task]
            assert len(conv_elem_l) == 1
            assert orig_elem == conv_elem_l[0]

    def test_check_check_code_of_add_problem(self, setup_and_teardown, convert_key_data_to_prob_data):
        config = setup_and_teardown
        config_mode = "Test"
        root_data_dir = config[config_mode]["root_data_dir"]
        root_output_dir = config[config_mode]["root_output_dir"]
        # prob_data_subdir = config[config_mode]["prob_data_subdir"]
        # prob_data_dir = os.path.join(root_dir, prob_data_subdir)
        output_subdir = config[config_mode]["script_output_subdir"]
        prob_json_fp = os.path.join(root_data_dir,
                                    "practice_problem_data/prob_data_from_key_data_output"
                                    ".json")
        prob_json_conv_fp = os.path.join(root_output_dir, output_subdir, "output_convert_key_data_to_prob_data",
                                         "warmup.json")
        orig_json = open(prob_json_fp, "r")
        orig_data = json.load(orig_json)
        conv_json = open(prob_json_conv_fp, "r")
        conv_data = json.load(conv_json)
        orig_codes = orig_data["code_list"]
        conv_codes = conv_data["code_list"]
        orig_add = [elem for elem in orig_codes if elem["trial_id"] == '00001_add'][0]
        conv_add = [elem for elem in conv_codes if elem["trial_id"] == '00001_add'][0]
        assert orig_add['specification'] == conv_add['specification']
        # assert orig_add['code_given'] == conv_add['code_given']
        assert orig_add['prompt_fixed'] == conv_add['prompt_fixed']
        assert orig_add == conv_add
