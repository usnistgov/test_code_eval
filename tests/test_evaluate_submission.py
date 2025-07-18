import pytest
import sys
import os
import configparser
import numpy as np
import pandas as pd

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)
pd.set_option("display.max_colwidth", 200)

sys.path.insert(0, "../genai_code_test")
import genai_code_test.evaluation_environment.evaluate_submission


print("Paths start")
for p in sys.path:
    print(p)
print("Paths end")


class TestSubmissionMix1(object):
    """
    Pytest class that tests a selection of real system outputs from preliminary run
    """

    @pytest.fixture
    def score_test_mix_2(self):
        config_filepath = os.environ["GENAI_CODE_CONFIG_PATH"]
        config_mode = "Test"
        try:
            config = configparser.ConfigParser()
            with open(config_filepath) as configfile:
                config.read_file(configfile)
        except ImportError:
            sys.exit("Cannot open config file: " + config_filepath)

        # Read root directories from config file
        # root_repo_dir = config[config_mode]["root_repo_dir"]
        root_data_dir = config[config_mode]["root_data_dir"]
        root_submissions_dir = config[config_mode]["root_submissions_dir"]
        root_working_dir = config[config_mode]["root_working_dir"]
        root_output_dir = config[config_mode]["root_output_dir"]

        key_data_subdir = config[config_mode]["key_data_subdir"]
        key_data_dir = os.path.join(root_data_dir, key_data_subdir)
        key_json_filepath = os.path.join(key_data_dir, "key_smoke_v0d95.json")
        submissions_dir = root_submissions_dir
        submission_json_filepath = os.path.join(submissions_dir, "test_mix_1", "baseline_two_test_v0d95.json")
        temp_working_dir = os.path.join(root_working_dir)
        eval_output_subdir = config[config_mode]["eval_output_subdir"]
        output_dir = os.path.join(root_output_dir, eval_output_subdir)

        verbose = True
        # Fix the datetime information to an arbitrary date so we always look into the same directory
        str_current_datetime = "2025-01-01-T01-01-01"
        sys_scores_fp = os.path.join(output_dir,
                                     "2025-01-01-T01-01-01-outputs/nist_baseline_two_test_code"
                                     "/nist_baseline_two_test_code_scores.csv")
        genai_code_test.evaluation_environment.evaluate_submission.evaluate_code_submission(
            str_current_datetime=str_current_datetime,
            key_json_filepath=key_json_filepath,
            submission_json_filepath=submission_json_filepath,
            temp_test_dir=temp_working_dir,
            output_dir=output_dir,
            system_name="",
            verbose=verbose,
        )
        sys_scores2 = pd.read_csv(sys_scores_fp)
        return sys_scores2

    @pytest.fixture
    def score_test_mix_3(self):
        config_filepath = os.environ["GENAI_CODE_CONFIG_PATH"]
        config_mode = "Test"
        try:
            config = configparser.ConfigParser()
            with open(config_filepath) as configfile:
                config.read_file(configfile)
        except ImportError:
            sys.exit("Cannot open config file: " + config_filepath)

        # Read root directories from config file
        # root_repo_dir = config[config_mode]["root_repo_dir"]
        root_data_dir = config[config_mode]["root_data_dir"]
        root_submissions_dir = config[config_mode]["root_submissions_dir"]
        root_working_dir = config[config_mode]["root_working_dir"]
        root_output_dir = config[config_mode]["root_output_dir"]

        key_data_subdir = config[config_mode]["key_data_subdir"]
        key_data_dir = os.path.join(root_data_dir, key_data_subdir)
        key_json_filepath = os.path.join(key_data_dir, "key_smoke_v0d95.json")
        submissions_dir = root_submissions_dir
        submission_json_filepath = os.path.join(submissions_dir, "test_mix_1", "baseline_reference_v0d95.json")
        temp_working_dir = os.path.join(root_working_dir)
        eval_output_subdir = config[config_mode]["eval_output_subdir"]
        output_dir = os.path.join(root_output_dir, eval_output_subdir)

        verbose = True
        # Fix the datetime information to an arbitrary date so we always look into the same directory
        str_current_datetime = "2025-03-01-T01-01-01"
        sys_scores_fp = os.path.join(output_dir,
                                     "2025-03-01-T01-01-01-outputs/nist_baseline_reference_code"
                                     "/nist_baseline_reference_code_scores.csv")
        genai_code_test.evaluation_environment.evaluate_submission.evaluate_code_submission(
            str_current_datetime=str_current_datetime,
            key_json_filepath=key_json_filepath,
            submission_json_filepath=submission_json_filepath,
            temp_test_dir=temp_working_dir,
            output_dir=output_dir,
            system_name="",
            verbose=verbose
        )
        sys_scores3 = pd.read_csv(sys_scores_fp)
        return sys_scores3

    @pytest.fixture
    def score_test_mix_4(self):
        config_filepath = os.environ["GENAI_CODE_CONFIG_PATH"]
        config_mode = "Test"
        try:
            config = configparser.ConfigParser()
            with open(config_filepath) as configfile:
                config.read_file(configfile)
        except ImportError:
            sys.exit("Cannot open config file: " + config_filepath)

        # Read root directories from config file
        # root_repo_dir = config[config_mode]["root_repo_dir"]
        root_data_dir = config[config_mode]["root_data_dir"]
        root_submissions_dir = config[config_mode]["root_submissions_dir"]
        root_working_dir = config[config_mode]["root_working_dir"]
        root_output_dir = config[config_mode]["root_output_dir"]

        key_data_subdir = config[config_mode]["key_data_subdir"]
        key_data_dir = os.path.join(root_data_dir, key_data_subdir)
        key_json_filepath = os.path.join(key_data_dir, "key_smoke_v0d99.json")
        submissions_dir = root_submissions_dir
        submission_json_filepath = os.path.join(submissions_dir, "test_mix_1", "part_of_baseline_mprompt.json")
        temp_working_dir = os.path.join(root_working_dir)
        eval_output_subdir = config[config_mode]["eval_output_subdir"]
        output_dir = os.path.join(root_output_dir, eval_output_subdir)

        verbose = True
        # Fix the datetime information to an arbitrary date so we always look into the same directory
        str_current_datetime = "2025-03-03-T10-10-10"
        sys_scores_fp = os.path.join(output_dir,
                                     "2025-03-03-T10-10-10-outputs/nist_baseline_reference_code"
                                     "/nist_baseline_reference_code_scores.csv")
        genai_code_test.evaluation_environment.evaluate_submission.evaluate_code_submission(
            str_current_datetime=str_current_datetime,
            key_json_filepath=key_json_filepath,
            submission_json_filepath=submission_json_filepath,
            temp_test_dir=temp_working_dir,
            output_dir=output_dir,
            system_name="",
            verbose=verbose
        )
        sys_scores4 = pd.read_csv(sys_scores_fp)
        return sys_scores4

    def test_mix_inputs2(self, score_test_mix_2):
        """
        Test of first mix of outputs
        """
        sys_scores2 = score_test_mix_2
        assert sys_scores2.loc[sys_scores2["trial_id"] == "00001_add", "correct_tests"].iloc[0] == 1
        assert sys_scores2.loc[sys_scores2["trial_id"] ==
                               "00002_heap_queue_largest", "finds_error_in_incorrect_t"].iloc[0] == 1
        assert (sys_scores2.loc[sys_scores2["trial_id"] == "00004_unique", "finds_error_in_incorrect_t"].iloc[0] == 1)
        assert sys_scores2.loc[sys_scores2["trial_id"] == "00003_make_palindrome", "correct_tests"].iloc[0] == 1

    def test_mix_inputs3(self, score_test_mix_3):
        """
        Test of first mix of outputs
        """
        sys_scores3 = score_test_mix_3
        assert sys_scores3.loc[sys_scores3["trial_id"] == "00001_add", "correct_tests"].iloc[0] == 1
        assert sys_scores3.loc[sys_scores3["trial_id"] == "00004_unique", "correct_tests"].iloc[0] == 1
        assert (sys_scores3.loc[sys_scores3["trial_id"] ==
                                "00002_heap_queue_largest", "finds_error_in_incorrect_1"].iloc[0] == 1)
        assert sys_scores3.loc[sys_scores3["trial_id"] ==
                               "00003_make_palindrome", "finds_error_in_incorrect_t"].iloc[0] == 1

    def test_mix_inputs4(self, score_test_mix_4):
        """
        Test of first mix of outputs
        """
        sys_scores4 = score_test_mix_4
        assert sys_scores4.loc[((sys_scores4["trial_id"] == "00001_add") & (sys_scores4["prompt_number"] == 0),
                                "correct_tests")].iloc[0] == 1
        assert sys_scores4.loc[((sys_scores4["trial_id"] == "00001_add") & (sys_scores4["prompt_number"] == 1),
                                "finds_error_in_incorrect_t")].iloc[0] == 1
        assert sys_scores4.loc[((sys_scores4["trial_id"] == "00004_unique") & (sys_scores4["prompt_number"] == 0),
                                "finds_error_in_incorrect_1")].iloc[0] == 1
        assert sys_scores4.loc[((sys_scores4["trial_id"] == "00004_unique") & (sys_scores4["prompt_number"] == 7),
                                "finds_error_in_incorrect_1")].iloc[0] == 1

    def test_xfail_inputs2(self, score_test_mix_2):
        sys_scores = score_test_mix_2
        assert sys_scores.loc[sys_scores["trial_id"] == "00001_add", "finds_error_in_incorrect_t"].iloc[0] == 1
        assert sys_scores.loc[sys_scores["trial_id"] == "00002_heap_queue_largest",
                                                        "finds_error_in_incorrect_1"].iloc[0] == 1
        assert sys_scores.loc[sys_scores["trial_id"] == "00004_unique", "finds_error_in_incorrect_1"].iloc[0] == 1

    def test_xfail_inputs3(self, score_test_mix_3):
        sys_scores = score_test_mix_3
        assert sys_scores.loc[sys_scores["trial_id"] == "00002_heap_queue_largest", "correct_tests"].iloc[0] == 1
        assert sys_scores.loc[sys_scores["trial_id"] == "00003_make_palindrome", "correct_tests"].iloc[0] == 1


class TestAddsUp(object):

    @pytest.fixture
    def score_test_adds(self):
        config_filepath = os.environ["GENAI_CODE_CONFIG_PATH"]
        config_mode = "Test"
        try:
            config = configparser.ConfigParser()
            with open(config_filepath) as configfile:
                config.read_file(configfile)
        except ImportError:
            sys.exit("Cannot open config file: " + config_filepath)

        # Read root directories from config file
        # root_repo_dir = config[config_mode]["root_repo_dir"]
        root_data_dir = config[config_mode]["root_data_dir"]
        root_submissions_dir = config[config_mode]["root_submissions_dir"]
        root_working_dir = config[config_mode]["root_working_dir"]
        root_output_dir = config[config_mode]["root_output_dir"]

        key_data_subdir = config[config_mode]["key_data_subdir"]
        key_data_dir = os.path.join(root_data_dir, key_data_subdir)
        key_json_filepath = os.path.join(key_data_dir, "key_add_up.json")
        submissions_dir = root_submissions_dir
        submission_json_filepath = os.path.join(submissions_dir, "test_add_up", "submission_smoke_fixed.json")
        temp_working_dir = os.path.join(root_working_dir)
        eval_output_subdir = config[config_mode]["eval_output_subdir"]
        output_dir = os.path.join(root_output_dir, eval_output_subdir)

        verbose = True
        # Fix the datetime information to an arbitrary date so we always look into the same directory
        str_current_datetime = "2025-02-26-T20-22-25"
        sys_scores_fp = os.path.join(output_dir, "2025-02-26-T20-22-25-outputs/add_up/add_up_scores.csv")
        genai_code_test.evaluation_environment.evaluate_submission.evaluate_code_submission(
            str_current_datetime=str_current_datetime,
            key_json_filepath=key_json_filepath,
            submission_json_filepath=submission_json_filepath,
            temp_test_dir=temp_working_dir,
            output_dir=output_dir,
            system_name="",
            verbose=verbose
        )
        sys_scores = pd.read_csv(sys_scores_fp)
        return sys_scores

    def test_add_up(self, score_test_adds, setup_and_teardown):
        expected_scores = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1.0]
        assert score_test_adds["correct_tests"].to_list() == expected_scores


class TestAddsUpErr(object):

    @pytest.fixture
    def score_test_adds_err(self):
        config_filepath = os.environ["GENAI_CODE_CONFIG_PATH"]
        config_mode = "Test"
        try:
            config = configparser.ConfigParser()
            with open(config_filepath) as configfile:
                config.read_file(configfile)
        except ImportError:
            sys.exit("Cannot open config file: " + config_filepath)

        # Read root directories from config file
        # root_repo_dir = config[config_mode]["root_repo_dir"]
        root_data_dir = config[config_mode]["root_data_dir"]
        root_submissions_dir = config[config_mode]["root_submissions_dir"]
        root_working_dir = config[config_mode]["root_working_dir"]
        root_output_dir = config[config_mode]["root_output_dir"]

        key_data_subdir = config[config_mode]["key_data_subdir"]
        key_data_dir = os.path.join(root_data_dir, key_data_subdir)
        key_json_filepath = os.path.join(key_data_dir, "key_add_up.json")
        submissions_dir = root_submissions_dir
        submission_json_filepath = os.path.join(submissions_dir, "test_add_up", "submission_err_smoke_fixed.json")
        temp_working_dir = os.path.join(root_working_dir)
        eval_output_subdir = config[config_mode]["eval_output_subdir"]
        output_dir = os.path.join(root_output_dir, eval_output_subdir)

        verbose = True
        # Fix the datetime information to an arbitrary date so we always look into the same directory
        str_current_datetime = "2025-02-28-T20-22-25"
        sys_scores_fp = os.path.join(output_dir, "2025-02-28-T20-22-25-outputs/add_up/add_up_scores.csv")
        genai_code_test.evaluation_environment.evaluate_submission.evaluate_code_submission(
            str_current_datetime=str_current_datetime,
            key_json_filepath=key_json_filepath,
            submission_json_filepath=submission_json_filepath,
            temp_test_dir=temp_working_dir,
            output_dir=output_dir,
            system_name="",
            verbose=verbose
        )
        sys_scores = pd.read_csv(sys_scores_fp)
        return sys_scores

    def test_add_up_err(self, score_test_adds_err, setup_and_teardown):
        expected_scores = [1.0, 0.0, 1.0, 0.0, 0.0, 0.0, np.nan, np.nan, 1, 0, 0, 0, 0, -1.0]
        np.testing.assert_equal(score_test_adds_err["correct_tests"].to_list(), expected_scores)


class TestSmokeExamples():

    @pytest.fixture
    def score_test_smoke_1(self, setup_and_teardown):
        config = setup_and_teardown
        config_mode = "Test"

        root_data_dir = config[config_mode]["root_data_dir"]
        root_submissions_dir = config[config_mode]["root_submissions_dir"]
        root_working_dir = config[config_mode]["root_working_dir"]
        root_output_dir = config[config_mode]["root_output_dir"]

        key_data_subdir = config[config_mode]["key_data_subdir"]
        key_data_dir = os.path.join(root_data_dir, key_data_subdir)
        key_json_filepath = os.path.join(key_data_dir, "key_smoke_v1d00.json")
        submissions_dir = root_submissions_dir
        submission_json_filepath = os.path.join(submissions_dir, "test_smoke_various", "test1_smoke.json")
        temp_working_dir = os.path.join(root_working_dir)
        eval_output_subdir = config[config_mode]["eval_output_subdir"]
        output_dir = os.path.join(root_output_dir, eval_output_subdir)

        verbose = True
        # Fix the datetime information to an arbitrary date so we always look into the same directory
        str_current_datetime = "2025-05-14-T01-01-01"
        sys_scores_fp = os.path.join(output_dir, "2025-05-14-T01-01-01-outputs/test1/test1_scores.csv")
        genai_code_test.evaluation_environment.evaluate_submission.evaluate_code_submission(
            str_current_datetime=str_current_datetime,
            key_json_filepath=key_json_filepath,
            submission_json_filepath=submission_json_filepath,
            temp_test_dir=temp_working_dir,
            output_dir=output_dir,
            system_name="",
            verbose=verbose,
        )
        sys_scores = pd.read_csv(sys_scores_fp)
        return sys_scores

    @pytest.fixture
    def score_test_smoke_1_v2(self, setup_and_teardown):
        config = setup_and_teardown
        config_mode = "Test"

        root_data_dir = config[config_mode]["root_data_dir"]
        root_submissions_dir = config[config_mode]["root_submissions_dir"]
        root_working_dir = config[config_mode]["root_working_dir"]
        root_output_dir = config[config_mode]["root_output_dir"]

        key_data_subdir = config[config_mode]["key_data_subdir"]
        key_data_dir = os.path.join(root_data_dir, key_data_subdir)
        key_json_filepath = os.path.join(key_data_dir, "key_smoke_v1d00.json")
        submissions_dir = root_submissions_dir
        submission_json_filepath = os.path.join(submissions_dir, "test_smoke_various", "test1_smoke.json")
        temp_working_dir = os.path.join(root_working_dir)
        eval_output_subdir = config[config_mode]["eval_output_subdir"]
        output_dir = os.path.join(root_output_dir, eval_output_subdir)

        verbose = True
        # Fix the datetime information to an arbitrary date so we always look into the same directory
        str_current_datetime = "2025-06-11-T05-05-05"
        sys_scores_fp = os.path.join(output_dir, "2025-06-11-T05-05-05-outputs/57/57_scores.csv")
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
        sys_metrics = pd.read_csv(os.path.join(output_dir, "2025-06-11-T05-05-05-outputs/57/57_mean_metrics.csv"))
        return sys_scores, sys_metrics

    def test_smoke_1_scorer(self, setup_and_teardown, score_test_smoke_1):
        # config = setup_and_teardown
        score = score_test_smoke_1
        # Complete this test
        assert (score.loc[(score.trial_id == "00001_add") & (score.prompt_number == 0), ["correct_tests",
                "finds_error_in_incorrect_1", "finds_error_in_incorrect_t"]].iloc[0].tolist() == [0, 1, 1])
        assert (score.loc[(score.trial_id == "00001_add") & (score.prompt_number == 1), ["correct_tests",
                "finds_error_in_incorrect_1", "finds_error_in_incorrect_t"]].iloc[0].tolist() == [1, 1, 1])
        assert (score.loc[(score.trial_id == "00002_heap_queue_largest") & (score.prompt_number == 0),
                ["correct_tests", "finds_error_in_incorrect_1", "finds_error_in_incorrect_t"]].iloc[0].tolist()
                == [-1, -1, -1])
        # Idea: the lack of "import pytest" raises a NameError. This missing import should flag a -1 error, not
        # a failure
        # For the incorrect case, a failure is detected before the import error is detected
        assert score.loc[(score.trial_id == "00002_heap_queue_largest") &
                         (score.prompt_number == 1), ["correct_tests", "finds_error_in_incorrect_1",
                         "finds_error_in_incorrect_t"]].iloc[0].tolist() == [-1, 1, -1]
        assert score.loc[(score.trial_id == "00003_make_palindrome") &
                         (score.prompt_number == 0), ["correct_tests", "finds_error_in_incorrect_1",
                         "finds_error_in_incorrect_t"]].iloc[0].tolist() == [0, 1, 1]
        assert score.loc[(score.trial_id == "00003_make_palindrome") &
                         (score.prompt_number == 1), ["correct_tests", "finds_error_in_incorrect_1",
                         "finds_error_in_incorrect_t"]].iloc[0].tolist() == [-1, -1, -1]
        assert score.loc[(score.trial_id == "00004_unique") &
                         (score.prompt_number == 0), ["correct_tests", "finds_error_in_incorrect_1",
                         "finds_error_in_incorrect_t"]].iloc[0].tolist() == [0, 1, -1]
        assert score.loc[(score.trial_id == "00004_unique") &
                         (score.prompt_number == 1), ["correct_tests", "finds_error_in_incorrect_1",
                         "finds_error_in_incorrect_t"]].iloc[0].tolist() == [1, 0, 0]

    def test_smoke_1_scorer_v2(self, setup_and_teardown, score_test_smoke_1_v2):
        # config = setup_and_teardown
        score, metric = score_test_smoke_1_v2
        # Complete this test
        assert (score.loc[(score.trial_id == "00001_add") & (score.prompt_number == 0), ["correct_tests",
                "finds_error_in_incorrect_1", "finds_error_in_incorrect_t"]].iloc[0].tolist() == [0, 1, 1])
        assert (score.loc[(score.trial_id == "00001_add") & (score.prompt_number == 1), ["correct_tests",
                "finds_error_in_incorrect_1", "finds_error_in_incorrect_t"]].iloc[0].tolist() == [1, 1, 1])
        assert (score.loc[(score.trial_id == "00002_heap_queue_largest") & (score.prompt_number == 0),
                ["correct_tests", "finds_error_in_incorrect_1", "finds_error_in_incorrect_t"]].iloc[0].tolist()
                == [-1, -1, -1])
        # Idea: the lack of "import pytest" raises a NameError. This missing import should flag a -1 error, not
        # a failure
        # For the incorrect case, a failure is detected before the import error is detected
        assert score.loc[(score.trial_id == "00002_heap_queue_largest") &
                         (score.prompt_number == 1), ["correct_tests", "finds_error_in_incorrect_1",
                         "finds_error_in_incorrect_t"]].iloc[0].tolist() == [-1, 1, -1]
        assert score.loc[(score.trial_id == "00003_make_palindrome") &
                         (score.prompt_number == 0), ["correct_tests", "finds_error_in_incorrect_1",
                         "finds_error_in_incorrect_t"]].iloc[0].tolist() == [0, 1, 1]
        assert score.loc[(score.trial_id == "00003_make_palindrome") &
                         (score.prompt_number == 1), ["correct_tests", "finds_error_in_incorrect_1",
                         "finds_error_in_incorrect_t"]].iloc[0].tolist() == [-1, -1, -1]
        assert score.loc[(score.trial_id == "00004_unique") &
                         (score.prompt_number == 0), ["correct_tests", "finds_error_in_incorrect_1",
                         "finds_error_in_incorrect_t"]].iloc[0].tolist() == [0, 1, -1]
        assert score.loc[(score.trial_id == "00004_unique") &
                         (score.prompt_number == 1), ["correct_tests", "finds_error_in_incorrect_1",
                         "finds_error_in_incorrect_t"]].iloc[0].tolist() == [1, 0, 0]
        # Test the system field for the score data frame
        assert pd.unique(score['system']).tolist() == [57]
        # Test the mean metrics data frane
        assert pd.unique(metric['system']).tolist() == [57]
        assert (metric.loc[metric.prompt_number == 0, ["correct_tests", "finds_cit_error",
                                                       "finds_ci1_and_cit_errors", "finds_cit_error",
                                                       "full_coverage_and_finds_all_errors"]].iloc[0].tolist() == [
            0, 0, 0, 0, 0])
        assert (metric.loc[metric.prompt_number == 1, ["correct_tests", "finds_ci1_error",
                                                       "finds_ci1_and_cit_errors", "finds_cit_error",
                                                       "full_coverage_and_finds_all_errors"]].iloc[0].tolist() == [
            50.0, 25.0, 25.0, 25.0, 25.0])
