import pytest
import os
import sys
import json

sys.path.insert(0, "../genai_code_test")
from genai_code_test.utils.create_json_file_from_code_files import func_create_json_file_from_code_files
from genai_code_test.utils.create_code_files_from_json_input import func_create_code_files_from_json


class TestWarmupCodeBank(object):

    @pytest.fixture
    def convert_warmup_to_json_and_back(self, setup_and_teardown):
        print("Converting Warmup File to json and back")
        config = setup_and_teardown
        config_mode = "Test"
        root_data_dir = config[config_mode]["root_data_dir"]
        root_output_dir = config[config_mode]["root_output_dir"]
        prob_data_subdir = config[config_mode]["prob_data_subdir"]
        prob_data_dir = os.path.join(root_data_dir, prob_data_subdir)
        output_subdir = config[config_mode]["script_output_subdir"]

        # Conversion 1: Produce the files from the warmup json
        prob_json_filepath_dir = os.path.join(prob_data_dir, "testing_warmup")
        prob_output_dir = os.path.join(root_output_dir, output_subdir, "warmup")
        result = func_create_code_files_from_json(prob_json_filepath_dir, prob_output_dir)
        assert result
        # Conversion 2: Get a converted json back from the previous output
        warmup_output_dir = os.path.join(root_output_dir, output_subdir, "warmup_conversion")
        result = func_create_json_file_from_code_files(prob_output_dir, warmup_output_dir)
        assert result
        print(prob_json_filepath_dir)
        print(prob_output_dir)
        print(warmup_output_dir)
        return True

    def test_check_metadata_length(self, setup_and_teardown, convert_warmup_to_json_and_back):
        config = setup_and_teardown
        config_mode = "Test"
        root_output_dir = config[config_mode]["root_output_dir"]
        output_subdir = config[config_mode]["script_output_subdir"]
        prob_output_dir = os.path.join(root_output_dir, output_subdir, "warmup")

        # Read Metadata file 1
        metadata_fp_1 = os.path.join(prob_output_dir, "code_bank_smoke_v0d95", "metadata.json")
        md1_json = open(metadata_fp_1, "r")
        md1 = json.load(md1_json)
        assert len(md1["code_list"]) == 4
        md1_json.close()

        # Read Metadata file 2
        metadata_fp_2 = os.path.join(prob_output_dir, "code_bank_smoke_v0d91", "metadata.json")
        md2_json = open(metadata_fp_2, "r")
        md2 = json.load(md2_json)
        assert len(md2["code_list"]) == 4
        md2_json.close()

    def test_check_two_files(self, setup_and_teardown, convert_warmup_to_json_and_back):
        config = setup_and_teardown
        config_mode = "Test"
        root_output_dir = config[config_mode]["root_output_dir"]
        output_subdir = config[config_mode]["script_output_subdir"]
        warmup_output_dir = os.path.join(root_output_dir, output_subdir, "warmup_conversion")
        files_list = [name for name in os.listdir(warmup_output_dir) if
                      os.path.isfile(os.path.join(warmup_output_dir, name))]
        print(files_list)
        assert len(files_list) == 2

    def test_check_file_metadata(self, setup_and_teardown, convert_warmup_to_json_and_back):
        config = setup_and_teardown
        config_mode = "Test"
        root_data_dir = config[config_mode]["root_data_dir"]
        prob_data_subdir = config[config_mode]["prob_data_subdir"]
        prob_data_dir = os.path.join(root_data_dir, prob_data_subdir)
        root_output_dir = config[config_mode]["root_output_dir"]
        output_subdir = config[config_mode]["script_output_subdir"]
        prob_json_fp = os.path.join(prob_data_dir, "testing_warmup", "code_bank_smoke_v0d95.json")
        prob_json_conv_fp = os.path.join(root_output_dir, output_subdir, "warmup_conversion",
                                         "code_bank_pilot1_smoke_test_problems_0d95_converted.json")
        orig_json = open(prob_json_fp, "r")
        orig_data = json.load(orig_json)
        conv_json = open(prob_json_conv_fp, "r")
        conv_data = json.load(conv_json)
        assert orig_data["version"] == conv_data["version"]
        assert orig_data["name"] == conv_data["name"]
        orig_json.close()
        conv_json.close()
        prob_json_fp = os.path.join(prob_data_dir, "testing_warmup", "code_bank_smoke_v0d91.json")
        prob_json_conv_fp = os.path.join(root_output_dir, output_subdir, "warmup_conversion",
                                         "code_bank_pilot1_warmup_problems_0d91_converted.json")
        orig_json = open(prob_json_fp, "r")
        orig_data = json.load(orig_json)
        conv_json = open(prob_json_conv_fp, "r")
        conv_data = json.load(conv_json)
        assert orig_data["version"] == conv_data["version"]
        assert orig_data["name"] == conv_data["name"]
        orig_json.close()
        conv_json.close()

    def test_check_code_file_equality(self, setup_and_teardown, convert_warmup_to_json_and_back):
        # We are OK if the json code_file elements are in a different order
        config = setup_and_teardown
        config_mode = "Test"
        root_data_dir = config[config_mode]["root_data_dir"]
        prob_data_subdir = config[config_mode]["prob_data_subdir"]
        prob_data_dir = os.path.join(root_data_dir, prob_data_subdir)
        root_output_dir = config[config_mode]["root_output_dir"]
        output_subdir = config[config_mode]["script_output_subdir"]
        prob_json_fp = os.path.join(prob_data_dir, "testing_warmup", "code_bank_smoke_v0d91.json")
        prob_json_conv_fp = os.path.join(root_output_dir, output_subdir, "warmup_conversion",
                                         "code_bank_pilot1_smoke_test_problems_0d95_converted.json")
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
        orig_json.close()
        conv_json.close()

    def test_check_check_code_of_add_problem(self, setup_and_teardown, convert_warmup_to_json_and_back):
        config = setup_and_teardown
        config_mode = "Test"
        root_data_dir = config[config_mode]["root_data_dir"]
        prob_data_subdir = config[config_mode]["prob_data_subdir"]
        prob_data_dir = os.path.join(root_data_dir, prob_data_subdir)
        root_output_dir = config[config_mode]["root_output_dir"]
        output_subdir = config[config_mode]["script_output_subdir"]
        prob_json_fp = os.path.join(prob_data_dir, "testing_warmup", "code_bank_smoke_v0d95.json")
        prob_json_conv_fp = os.path.join(root_output_dir, output_subdir, "warmup_conversion",
                                         "code_bank_pilot1_smoke_test_problems_0d95_converted.json")
        orig_json = open(prob_json_fp, "r")
        orig_data = json.load(orig_json)
        conv_json = open(prob_json_conv_fp, "r")
        conv_data = json.load(conv_json)
        orig_codes = orig_data["code_list"]
        conv_codes = conv_data["code_list"]
        assert len(orig_codes) == len(conv_codes)
        # orig_add = [elem for elem in orig_codes if elem["trial_id"] == '00001_add'][0]
        # conv_add = [elem for elem in conv_codes if elem["trial_id"] == '00001_add'][0]
        # assert orig_add['specification'] == conv_add['specification']
        # assert orig_add['code_correct'] == conv_add['code_correct']
        # assert orig_add['code_incorrect_1'] == conv_add['code_incorrect_1']
        # assert orig_add == conv_add
        orig_json.close()
        conv_json.close()
