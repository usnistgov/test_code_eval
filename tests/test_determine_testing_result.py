import pytest
import sys
import os
import pandas as pd

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)
pd.set_option("display.max_colwidth", 200)

sys.path.insert(0, "../genai_code_test")
import genai_code_test.evaluation_environment.evaluate_submission
from genai_code_test.evaluation_environment.validate_submission import determine_testing_result


class TestDetermineSmokeExamples():

    @pytest.fixture
    def score_test_dry_1f(self, setup_and_teardown):
        config = setup_and_teardown
        config_mode = "Test"

        root_data_dir = config[config_mode]["root_data_dir"]
        root_submissions_dir = config[config_mode]["root_submissions_dir"]
        root_working_dir = config[config_mode]["root_working_dir"]
        root_output_dir = config[config_mode]["root_output_dir"]

        key_data_subdir = config[config_mode]["key_data_subdir"]
        key_data_dir = os.path.join(root_data_dir, key_data_subdir)
        key_json_filepath = os.path.join(key_data_dir, "key_dry_v2d00.json")
        submissions_dir = root_submissions_dir
        submission_json_filepath = os.path.join(submissions_dir, "test_determine", "test1f_dry.json")
        temp_working_dir = os.path.join(root_working_dir)
        eval_output_subdir = config[config_mode]["eval_output_subdir"]
        output_dir = os.path.join(root_output_dir, eval_output_subdir)

        verbose = True
        # Fix the datetime information to an arbitrary date so we always look into the same directory
        str_current_datetime = "2026-04-23-T05-05-05"
        sys_scores_fp = os.path.join(output_dir, "2026-04-23-T05-05-05-outputs/57/57_scores.csv")
        genai_code_test.evaluation_environment.evaluate_submission.evaluate_code_submission(
            str_current_datetime=str_current_datetime,
            key_json_filepath=key_json_filepath,
            submission_json_filepath=submission_json_filepath,
            temp_test_dir=temp_working_dir,
            output_dir=output_dir,
            system_name="57",
            verbose=verbose,
        )
        sys_scores = pd.read_csv(sys_scores_fp)
        sys_metrics = pd.read_csv(os.path.join(output_dir, "2026-04-23-T05-05-05-outputs/57/57_mean_metrics.csv"))
        eval_outputs_dir = os.path.join(output_dir, "2026-04-23-T05-05-05-outputs", "57")
        return sys_scores, sys_metrics, eval_outputs_dir

    def test_dry_1e_determine_add(self, setup_and_teardown, score_test_dry_1f):
        """ Extract the Pytest Output from the files and check the determine_testing_result """
        score, metric, eval_outputs_dir = score_test_dry_1f
        # 00001_add
        add_0c_fpath = os.path.join(eval_outputs_dir, "00001_add2", "pytest_output_00001_add2_0_57_correct_fixed.txt")
        with open(add_0c_fpath, 'r') as file:
            add_0c_tstr = file.read()
        expected_output = 1
        obtained_output = determine_testing_result(add_0c_tstr)
        assert obtained_output == expected_output
        add_1c_fpath = os.path.join(eval_outputs_dir, "00001_add2", "pytest_output_00001_add2_1_57_correct_custom.txt")
        with open(add_1c_fpath, 'r') as file:
            add_1c_tstr = file.read()
        expected_output = 1
        obtained_output = determine_testing_result(add_1c_tstr)
        assert obtained_output == expected_output
        add_2c_fpath = os.path.join(eval_outputs_dir, "00001_add2", "pytest_output_00001_add2_2_57_correct_custom.txt")
        with open(add_2c_fpath, 'r') as file:
            add_2c_tstr = file.read()
        expected_output = 1
        obtained_output = determine_testing_result(add_2c_tstr)
        assert obtained_output == expected_output

    def test_dry_1e_determine_heap(self, setup_and_teardown, score_test_dry_1f):
        """ Extract the Pytest Output from the files and check the determine_testing_result """
        score, metric, eval_outputs_dir = score_test_dry_1f
        # 00002_heap_queue_largest
        heap_0c_fpath = os.path.join(
            eval_outputs_dir,
            "00002_heap_queue_largest2",
            "pytest_output_00002_heap_queue_largest2_0_57_correct_fixed.txt")
        with open(heap_0c_fpath, 'r') as file:
            heap_0c_tstr = file.read()
        expected_output = -1
        obtained_output = determine_testing_result(heap_0c_tstr)
        assert obtained_output == expected_output
        heap_1c_fpath = os.path.join(
            eval_outputs_dir,
            "00002_heap_queue_largest2",
            "pytest_output_00002_heap_queue_largest2_1_57_correct_custom.txt")
        with open(heap_1c_fpath, 'r') as file:
            heap_1c_tstr = file.read()
        expected_output = -1
        obtained_output = determine_testing_result(heap_1c_tstr)
        assert obtained_output == expected_output

    def test_dry_1e_determine_palindrome(self, setup_and_teardown, score_test_dry_1f):
        """ Extract the Pytest Output from the files and check the determine_testing_result """
        score, metric, eval_outputs_dir = score_test_dry_1f
        # 00003_make_palindrome
        pal_0c_fpath = os.path.join(
            eval_outputs_dir,
            "00003_make_palindrome2",
            "pytest_output_00003_make_palindrome2_0_57_correct_fixed.txt")
        with open(pal_0c_fpath, 'r') as file:
            pal_0c_tstr = file.read()
        expected_output = 0
        obtained_output = determine_testing_result(pal_0c_tstr)
        assert obtained_output == expected_output
        pal_1c_fpath = os.path.join(
            eval_outputs_dir,
            "00003_make_palindrome2",
            "pytest_output_00003_make_palindrome2_1_57_correct_custom.txt")
        with open(pal_1c_fpath, 'r') as file:
            pal_1c_tstr = file.read()
        expected_output = -1
        obtained_output = determine_testing_result(pal_1c_tstr)
        assert obtained_output == expected_output

    def test_dry_1e_determine_unique(self, setup_and_teardown, score_test_dry_1f):
        """ Extract the Pytest Output from the files and check the determine_testing_result """
        score, metric, eval_outputs_dir = score_test_dry_1f
        # 00004_unique
        uni_0c_fpath = os.path.join(
            eval_outputs_dir,
            "00004_unique2",
            "pytest_output_00004_unique2_0_57_correct_fixed.txt")
        with open(uni_0c_fpath, 'r') as file:
            uni_0c_tstr = file.read()
        expected_output = 0
        obtained_output = determine_testing_result(uni_0c_tstr)
        assert obtained_output == expected_output
        uni_1c_fpath = os.path.join(
            eval_outputs_dir,
            "00004_unique2",
            "pytest_output_00004_unique2_1_57_correct_custom.txt")
        with open(uni_1c_fpath, 'r') as file:
            uni_1c_tstr = file.read()
        expected_output = 1
        obtained_output = determine_testing_result(uni_1c_tstr)
        assert obtained_output == expected_output

    def test_dry_1e_scorer(self, setup_and_teardown, score_test_dry_1f):
        # config = setup_and_teardown
        score, metric, eval_outputs_dir = score_test_dry_1f
        # Complete this test
        assert (score.loc[(score.trial_id == "00001_add2") & (score.prompt_number == 0), ["correct_tests",
                "finds_error_in_incorrect_1", "finds_error_in_incorrect_t"]].iloc[0].tolist() == [1, 1, 1])
        assert (score.loc[(score.trial_id == "00001_add2") & (score.prompt_number == 1), ["correct_tests",
                "finds_error_in_incorrect_1", "finds_error_in_incorrect_t"]].iloc[0].tolist() == [1, 1, 1])
        assert (score.loc[(score.trial_id == "00001_add2") & (score.prompt_number == 2), ["correct_tests",
                "finds_error_in_incorrect_1", "finds_error_in_incorrect_t"]].iloc[0].tolist() == [1, 1, 1])
        assert (score.loc[(score.trial_id == "00002_heap_queue_largest2") & (score.prompt_number == 0),
                ["correct_tests", "finds_error_in_incorrect_1", "finds_error_in_incorrect_t"]].iloc[0].tolist()
                == [-1, -1, -1])
        # Idea: the lack of "import pytest" raises a NameError. This missing import should flag a -1 error, not
        # a failure
        # For the incorrect case, a failure is detected before the import error is detected
        assert score.loc[(score.trial_id == "00002_heap_queue_largest2") &
                         (score.prompt_number == 1), ["correct_tests", "finds_error_in_incorrect_1",
                         "finds_error_in_incorrect_t"]].iloc[0].tolist() == [-1, 1, -1]
        assert score.loc[(score.trial_id == "00003_make_palindrome2") &
                         (score.prompt_number == 0), ["correct_tests", "finds_error_in_incorrect_1",
                         "finds_error_in_incorrect_t"]].iloc[0].tolist() == [0, 1, 1]
        assert score.loc[(score.trial_id == "00003_make_palindrome2") &
                         (score.prompt_number == 1), ["correct_tests", "finds_error_in_incorrect_1",
                         "finds_error_in_incorrect_t"]].iloc[0].tolist() == [-1, -1, -1]
        assert score.loc[(score.trial_id == "00004_unique2") &
                         (score.prompt_number == 0), ["correct_tests", "finds_error_in_incorrect_1",
                         "finds_error_in_incorrect_t"]].iloc[0].tolist() == [0, 1, -1]
        assert score.loc[(score.trial_id == "00004_unique2") &
                         (score.prompt_number == 1), ["correct_tests", "finds_error_in_incorrect_1",
                         "finds_error_in_incorrect_t"]].iloc[0].tolist() == [1, 1, 1]
