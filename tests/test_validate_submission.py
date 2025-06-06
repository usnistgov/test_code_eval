import os
import sys

sys.path.insert(0, "../genai_code_test")
from genai_code_test.evaluation_environment.validate_submission import validate_code_submission


def test_validate_submission_mix_1(setup_and_teardown):
    # Checking by selected paths

    config = setup_and_teardown
    config_mode = "Test"
    verbose = False

    # Read root directories from config file
    # root_repo_dir = config[config_mode]["root_repo_dir"]
    root_data_dir = config[config_mode]["root_data_dir"]
    root_submissions_dir = config[config_mode]["root_submissions_dir"]
    root_working_dir = config[config_mode]["root_working_dir"]
    root_output_dir = config[config_mode]["root_output_dir"]

    prob_data_subdir = config[config_mode]["prob_data_subdir"]
    prob_data_dir = os.path.join(root_data_dir, prob_data_subdir)
    # converted_files_dir = os.path.join(root_data_dir, "expected_validator_output")
    submissions_dir = root_submissions_dir
    temp_working_dir = os.path.join(root_working_dir)
    validate_output_subdir = config[config_mode]["validate_output_subdir"]
    output_dir = os.path.join(root_output_dir, validate_output_subdir)

    # Check 1 - see if problem set and submission will return validated or not validated, should return false because
    # 026_HumanEval_26_remove_duplicates_sorted has a NameError --  took out 026_HumanEval_26_remove_duplicates_sorted
    # so should return true
    prob_json_filepath = os.path.join(prob_data_dir, "testing_new_validator", "problem_input_one.json")
    submission_json_filepath = os.path.join(submissions_dir, "test_mix_1",
                                            "testing_submission_new_validator", "new_submission.json")

    current_datetime = "2024-10-07-T30-30-30"
    str_current_datetime = str(current_datetime)

    result = validate_code_submission(str_current_datetime, prob_json_filepath, submission_json_filepath,
                                      temp_working_dir, output_dir, verbose)
    assert result == True

    # Check 2 - see what happens if submission set is bigger than problem set - this should return false
    temp_working_dir2 = temp_working_dir
    output_dir2 = output_dir
    verbose2 = True
    prob_json_filepath2 = os.path.join(prob_data_dir, "testing_validation_small_prob_set.json")
    submission_json_filepath2 = os.path.join(submissions_dir, "test_mix_1", "part_of_submission.json")
    current_datetime2 = "2024-10-08-T30-30-30"
    str_current_datetime2 = str(current_datetime2)

    result2 = validate_code_submission(str_current_datetime2, prob_json_filepath2, submission_json_filepath2,
                                       temp_working_dir2, output_dir2, verbose2)

    assert result2 == True

    # Check 3 - see what happens if problem set is bigger than submission set - this should return true because it is
    # just a warning message when this happens - now this is false because returns an error now
    temp_working_dir3 = temp_working_dir
    output_dir3 = output_dir
    verbose3 = True
    prob_json_filepath3 = os.path.join(prob_data_dir, "validation_large_prob_set.json")
    submission_json_filepath3 = os.path.join(submissions_dir, "test_mix_1", "small_submission.json")
    current_datetime3 = "2024-10-09-T30-30-30"
    str_current_datetime3 = str(current_datetime3)

    result3 = validate_code_submission(str_current_datetime3, prob_json_filepath3, submission_json_filepath3,
                                       temp_working_dir3, output_dir3, verbose3)

    assert result3 == False

    # Check 4 - see what happens if a submission has prompt empty - this should
    # return false because prompt needs to be not empty in order to be validated
    temp_working_dir4 = temp_working_dir
    output_dir4 = output_dir
    verbose4 = verbose

    current_datetime4 = "2024-10-10-30-30-30"
    str_current_datetime4 = str(current_datetime4)

    prob_json_filepath4 = os.path.join(prob_data_dir, "new_testing.json")
    submission_json_filepath4 = os.path.join(submissions_dir, "test_mix_1", "new_submission.json")

    result4 = validate_code_submission(str_current_datetime4, prob_json_filepath4, submission_json_filepath4,
                                       temp_working_dir4, output_dir4, verbose4)

    assert result4 == False

    # Check 15 - see what happens if test code is over 25,000 characters should return error
    temp_working_dir15 = temp_working_dir
    output_dir15 = output_dir
    verbose15 = verbose

    current_datetime4 = "2024-10-12-45-30-15"
    str_current_datetime15 = str(current_datetime4)

    prob_json_filepath15 = os.path.join(prob_data_dir, "smoke_char.json")
    submission_json_filepath15 = os.path.join(submissions_dir, "test_mix_1", "submission_char.json")

    result15 = validate_code_submission(str_current_datetime15, prob_json_filepath15, submission_json_filepath15,
                                        temp_working_dir15, output_dir15, verbose15)

    assert result15 == False

    # Check 6 - Peter Check One - changed from Peter's comment - should return true because no result from test_given
    # returns -1
    temp_working_dir6 = temp_working_dir
    output_dir6 = output_dir
    verbose6 = verbose

    current_datetime6 = "2024-10-11-T30-30-30"
    str_current_datetime6 = str(current_datetime6)

    prob_json_filepath6 = os.path.join(prob_data_dir, "set_of_prob_inputs0d95_prob_set.json")
    submission_json_filepath6 = os.path.join(submissions_dir, "test_mix_1", "set_of_two_test_baseline.json")

    result6 = validate_code_submission(str_current_datetime6, prob_json_filepath6, submission_json_filepath6,
                                       temp_working_dir6, output_dir6, verbose6)
    assert result6 == True

    # Check 7 - See if it custom prompts required, should be true
    temp_working_dir7 = temp_working_dir
    output_dir7 = output_dir
    verbose7 = verbose

    current_datetime7 = "2024-10-11-T30-30-30"
    str_current_datetime7 = str(current_datetime7)

    prob_json_filepath7 = os.path.join(prob_data_dir, "data_version98.json")
    submission_json_filepath7 = os.path.join(submissions_dir, "test_mix_1", "sub_version_98.json")

    result7 = validate_code_submission(str_current_datetime7, prob_json_filepath7, submission_json_filepath7,
                                       temp_working_dir7, output_dir7, verbose7)
    assert result7 == True

    # Check 20 - See if it custom prompts required, should be false
    temp_working_dir20 = temp_working_dir
    output_dir20 = output_dir
    verbose20 = verbose

    current_datetime20 = "2024-10-11-T30-30-30"
    str_current_datetime20 = str(current_datetime20)

    prob_json_filepath20 = os.path.join(prob_data_dir, "incorrect_data_version98.json")
    submission_json_filepath20 = os.path.join(submissions_dir, "test_mix_1", "incorrect_sub_version_98.json")

    result20 = validate_code_submission(str_current_datetime20, prob_json_filepath20, submission_json_filepath20,
                                        temp_working_dir20, output_dir20, verbose20)
    assert result20 == False


def test_validate_submission_mix_2(setup_and_teardown):
    config = setup_and_teardown
    config_mode = "Test"

    verbose = False

    # Read root directories from config file
    # root_repo_dir = config[config_mode]["root_repo_dir"]
    root_data_dir = config[config_mode]["root_data_dir"]
    root_submissions_dir = config[config_mode]["root_submissions_dir"]
    root_working_dir = config[config_mode]["root_working_dir"]
    root_output_dir = config[config_mode]["root_output_dir"]

    prob_data_subdir = config[config_mode]["prob_data_subdir"]
    prob_data_dir = os.path.join(root_data_dir, prob_data_subdir)
    submissions_dir = root_submissions_dir
    temp_working_dir = os.path.join(root_working_dir)
    validate_output_subdir = config[config_mode]["validate_output_subdir"]
    output_dir = os.path.join(root_output_dir, validate_output_subdir)

    # Check 8 - Peter Check Three - should return false because at least one result from test_given is -1 -- should
    # return true because all problems are smoke test problems
    temp_working_dir8 = temp_working_dir
    output_dir8 = output_dir
    verbose8 = verbose
    prob_json_filepath8 = os.path.join(prob_data_dir, "test_prob_inputs_1_d95.json")
    submission_json_filepath8 = os.path.join(submissions_dir, "test_mix_2", "reference_submission.json")
    current_datetime8 = "2024-10-13-T30-30-30"
    str_current_datetime8 = str(current_datetime8)

    result8 = validate_code_submission(str_current_datetime8, prob_json_filepath8, submission_json_filepath8,
                                       temp_working_dir8, output_dir8, verbose8)
    assert result8 == True

    # Check to see if prompts match - should return true
    temp_working_dir10 = temp_working_dir
    output_dir10 = output_dir
    verbose10 = verbose
    prob_json_filepath10 = os.path.join(prob_data_dir, "testing_new_validator", "problem_file_one.json")
    submission_json_filepath10 = os.path.join(submissions_dir, "test_mix_1", "testing_submission_new_validator",
                                              "submission_file_one.json")
    current_datetime10 = "2024-10-23-T30-30-30"
    str_current_datetime10 = str(current_datetime10)

    result10 = validate_code_submission(str_current_datetime10, prob_json_filepath10, submission_json_filepath10,
                                        temp_working_dir10, output_dir10, verbose10)
    assert result10 == True

    # Check to see if prompts match - should return false
    temp_working_dir11 = temp_working_dir
    output_dir11 = output_dir
    verbose11 = verbose
    prob_json_filepath11 = os.path.join(prob_data_dir, "testing_new_validator", "problem_file_error_one.json")
    submission_json_filepath11 = os.path.join(submissions_dir, "test_mix_1", "testing_submission_new_validator",
                                              "submission_file_error_one.json")
    current_datetime11 = "2024-10-23-T30-30-30"
    str_current_datetime11 = str(current_datetime11)

    result11 = validate_code_submission(str_current_datetime11, prob_json_filepath11, submission_json_filepath11,
                                        temp_working_dir11, output_dir11, verbose11)
    assert result11 == False

    # Check to see if prompts match - should return True
    temp_working_dir12 = temp_working_dir
    output_dir12 = output_dir
    verbose12 = verbose
    prob_json_filepath12 = os.path.join(prob_data_dir, "testing_input_submission.json")
    submission_json_filepath12 = os.path.join(submissions_dir, "test_mix_1", "baseline_reference.json")
    current_datetime12 = "2024-11-23-T30-30-30"
    str_current_datetime12 = str(current_datetime12)

    result12 = validate_code_submission(str_current_datetime12, prob_json_filepath12, submission_json_filepath12,
                                        temp_working_dir12, output_dir12, verbose12)
    assert result12 == True

    # Check to see if prompts match - should return False
    temp_working_dir13 = temp_working_dir
    output_dir13 = output_dir
    verbose13 = verbose
    prob_json_filepath13 = os.path.join(prob_data_dir, "testing_input_submission.json")
    submission_json_filepath13 = os.path.join(submissions_dir, "test_mix_1", "baseline_two_test.json")
    current_datetime13 = "2024-12-30-T30-30-30"
    str_current_datetime13 = str(current_datetime13)

    result13 = validate_code_submission(str_current_datetime13, prob_json_filepath13, submission_json_filepath13,
                                        temp_working_dir13, output_dir13, verbose13)
    assert result13 == False

    # Check to see if you can validate custom and fixed together - should return false
    temp_working_dir14 = temp_working_dir
    output_dir14 = output_dir
    verbose14 = verbose
    prob_json_filepath14 = os.path.join(prob_data_dir, "input_v0d95.json")
    submission_json_filepath14 = os.path.join(submissions_dir, "test_mix_1", "baseline_reference_v0d95.json")
    current_datetime14 = "2025-12-30-T30-30-30"
    str_current_datetime14 = str(current_datetime14)

    result14 = validate_code_submission(str_current_datetime14, prob_json_filepath14, submission_json_filepath14,
                                        temp_working_dir14, output_dir14, verbose14)
    assert result14 == False


'''
def test_environment_check(setup_and_teardown):
    config = setup_and_teardown
    config_mode = "Test"

    verbose = True

    # Read root directories from config file
    # root_repo_dir = config[config_mode]["root_repo_dir"]
    root_data_dir = config[config_mode]["root_data_dir"]
    root_submissions_dir = config[config_mode]["root_submissions_dir"]
    root_working_dir = config[config_mode]["root_working_dir"]
    root_output_dir = config[config_mode]["root_output_dir"]

    prob_data_subdir = config[config_mode]["prob_data_subdir"]
    prob_data_dir = os.path.join(root_data_dir, prob_data_subdir)
    submissions_dir = root_submissions_dir
    temp_working_dir = os.path.join(root_working_dir)
    validate_output_subdir = config[config_mode]["validate_output_subdir"]
    output_dir = os.path.join(root_output_dir, validate_output_subdir)
    #Check 9 - Peter Check Four - making sure our environments are the same
    temp_working_dir9 = temp_working_dir
    output_dir9 = output_dir
    verbose9 = verbose
    prob_json_filepath9 = os.path.join(prob_data_dir, "test_prob_inputs_1_d95.json")
    submission_json_filepath9 = os.path.join(submissions_dir, "test_mix_2", "submission.json")
    current_datetime9 = "2024-10-01-T19-11-23"
    str_current_datetime9 = str(current_datetime9)

    result9 = validate_code_submission(str_current_datetime9, prob_json_filepath9, submission_json_filepath9,
                                       temp_working_dir9, output_dir9, verbose9)

    scores_filepath = os.path.join(output_dir9, str_current_datetime9 + "-outputs",
                                   "Test_Mix_2", "Test_Mix_2_validation.csv")
    scores_df = pd.read_csv(scores_filepath)
    ex_scores_col = [1.0, 1.0, 1.0]

    assert scores_df['test_given'].to_list() == ex_scores_col

    assert result9 == True
    '''

'''
def test_adds_up(setup_and_teardown):
    config = setup_and_teardown
    config_mode = "Test"

    verbose = True

    # Read root directories from config file
    # root_repo_dir = config[config_mode]["root_repo_dir"]
    root_data_dir = config[config_mode]["root_data_dir"]
    root_submissions_dir = config[config_mode]["root_submissions_dir"]
    root_working_dir = config[config_mode]["root_working_dir"]
    root_output_dir = config[config_mode]["root_output_dir"]

    prob_data_subdir = config[config_mode]["prob_data_subdir"]
    prob_data_dir = os.path.join(root_data_dir, prob_data_subdir)
    submissions_dir = root_submissions_dir
    temp_working_dir = os.path.join(root_working_dir)
    validate_output_subdir = config[config_mode]["validate_output_subdir"]
    output_dir = os.path.join(root_output_dir, validate_output_subdir)

    temp_working_dir9 = temp_working_dir
    output_dir9 = output_dir
    verbose9 = verbose
    prob_json_filepath9 = os.path.join(prob_data_dir, "input_add_up.json")
    submission_json_filepath9 = os.path.join(submissions_dir, "test_add_up", "submission_smoke_fixed.json")
    current_datetime = "2025-02-27-T20-22-25"
    str_current_datetime = str(current_datetime)

    validate_code_submission(str_current_datetime, prob_json_filepath9, submission_json_filepath9,
                             temp_working_dir9, output_dir9, verbose9)

    scores_filepath = os.path.join(output_dir9, str_current_datetime + "-outputs",
                                   "add_up", "add_up_validation.csv")
    scores_df = pd.read_csv(scores_filepath)
    expected_scores = [1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -1.0]
    assert scores_df['test_given'].to_list() == expected_scores
    '''


def test_adds_up_err(setup_and_teardown):
    config = setup_and_teardown
    config_mode = "Test"

    verbose = False

    # Read root directories from config file
    # root_repo_dir = config[config_mode]["root_repo_dir"]
    root_data_dir = config[config_mode]["root_data_dir"]
    root_submissions_dir = config[config_mode]["root_submissions_dir"]
    root_working_dir = config[config_mode]["root_working_dir"]
    root_output_dir = config[config_mode]["root_output_dir"]

    prob_data_subdir = config[config_mode]["prob_data_subdir"]
    prob_data_dir = os.path.join(root_data_dir, prob_data_subdir)
    submissions_dir = root_submissions_dir
    temp_working_dir = os.path.join(root_working_dir)
    validate_output_subdir = config[config_mode]["validate_output_subdir"]
    output_dir = os.path.join(root_output_dir, validate_output_subdir)

    temp_working_dir9 = temp_working_dir
    output_dir9 = output_dir
    verbose9 = verbose
    prob_json_filepath9 = os.path.join(prob_data_dir, "input_add_up.json")
    submission_json_filepath9 = os.path.join(submissions_dir, "test_add_up", "submission_err_smoke_fixed.json")
    current_datetime = "2025-02-22-T20-22-25"
    str_current_datetime = str(current_datetime)

    validate_code_submission(str_current_datetime, prob_json_filepath9, submission_json_filepath9,
                             temp_working_dir9, output_dir9, verbose9)

    log_filepath = os.path.join(output_dir9, str_current_datetime + "-outputs",
                                "validation_log.txt")
    with open(log_filepath, 'r') as file:
        log_data = file.read()
    assert ('ERROR: Please recheck the prompt and or prompt_number field, one of these are incorrect, please fix and '
            'try again!') in log_data

    # test for combined fixed and partial custom submission
    temp_working_dir10 = temp_working_dir
    output_dir10 = output_dir
    verbose10 = verbose
    prob_json_filepath10 = os.path.join(prob_data_dir, "testing_input_submission.json")
    submission_json_filepath10 = os.path.join(submissions_dir, "testing_sub.json")
    current_datetime = "2025-03-01-T01-01-01"
    str_current_datetime = str(current_datetime)

    validate_code_submission(str_current_datetime, prob_json_filepath10, submission_json_filepath10,
                             temp_working_dir10, output_dir10, verbose10)

    log_filepath = os.path.join(output_dir10, str_current_datetime + "-outputs",
                                "validation_log.txt")
    with open(log_filepath, 'r') as file:
        log_data = file.read()
    assert ('ERROR: Please recheck the prompt and or prompt_number field, one of these are incorrect, please fix and '
            'try again!') in log_data


def test_validate_smoke_submission(setup_and_teardown):
    config = setup_and_teardown
    config_mode = "Test"

    verbose = False

    # Read root directories from config file
    # root_repo_dir = config[config_mode]["root_repo_dir"]
    root_data_dir = config[config_mode]["root_data_dir"]
    root_submissions_dir = config[config_mode]["root_submissions_dir"]
    root_working_dir = config[config_mode]["root_working_dir"]
    root_output_dir = config[config_mode]["root_output_dir"]

    prob_data_subdir = config[config_mode]["prob_data_subdir"]
    prob_data_dir = os.path.join(root_data_dir, prob_data_subdir)
    submissions_dir = root_submissions_dir
    temp_working_dir = os.path.join(root_working_dir)
    validate_output_subdir = config[config_mode]["validate_output_subdir"]
    output_dir = os.path.join(root_output_dir, validate_output_subdir)

    temp_working_dir = temp_working_dir
    prob_json_filepath = os.path.join(prob_data_dir, "input_smoke_v1d00.json")
    submission_json_filepath = os.path.join(submissions_dir, "test_smoke_various", "test1_smoke.json")
    current_datetime = "2025-06-04-T01-01-01"
    str_current_datetime = str(current_datetime)
    result = validate_code_submission(str_current_datetime, prob_json_filepath, submission_json_filepath,
                                      temp_working_dir, output_dir, verbose)
    # In this case, check that this submission is valid
    assert result


def test_validate_bad_smoke_submission(setup_and_teardown):
    config = setup_and_teardown
    config_mode = "Test"

    verbose = False

    # Read root directories from config file
    # root_repo_dir = config[config_mode]["root_repo_dir"]
    root_data_dir = config[config_mode]["root_data_dir"]
    root_submissions_dir = config[config_mode]["root_submissions_dir"]
    root_working_dir = config[config_mode]["root_working_dir"]
    root_output_dir = config[config_mode]["root_output_dir"]

    prob_data_subdir = config[config_mode]["prob_data_subdir"]
    prob_data_dir = os.path.join(root_data_dir, prob_data_subdir)
    submissions_dir = root_submissions_dir
    temp_working_dir = os.path.join(root_working_dir)
    validate_output_subdir = config[config_mode]["validate_output_subdir"]
    output_dir = os.path.join(root_output_dir, validate_output_subdir)

    temp_working_dir = temp_working_dir
    prob_json_filepath = os.path.join(prob_data_dir, "input_smoke_v0d99.json")
    submission_json_filepath = os.path.join(submissions_dir, "test_smoke_various", "test1b_v0d99_smoke.json")
    current_datetime = "2025-06-04-T02-02-02"
    str_current_datetime = str(current_datetime)
    result = validate_code_submission(str_current_datetime, prob_json_filepath, submission_json_filepath,
                                      temp_working_dir, output_dir, verbose)
    # In this case, check that this submission is invalid as the prompt number is an integer, not a string
    assert not result


def test_validate_smoke3_submission(setup_and_teardown):
    config = setup_and_teardown
    config_mode = "Test"

    verbose = False

    # Read root directories from config file
    # root_repo_dir = config[config_mode]["root_repo_dir"]
    root_data_dir = config[config_mode]["root_data_dir"]
    root_submissions_dir = config[config_mode]["root_submissions_dir"]
    root_working_dir = config[config_mode]["root_working_dir"]
    root_output_dir = config[config_mode]["root_output_dir"]

    prob_data_subdir = config[config_mode]["prob_data_subdir"]
    prob_data_dir = os.path.join(root_data_dir, prob_data_subdir)
    submissions_dir = root_submissions_dir
    temp_working_dir = os.path.join(root_working_dir)
    validate_output_subdir = config[config_mode]["validate_output_subdir"]
    output_dir = os.path.join(root_output_dir, validate_output_subdir)

    temp_working_dir = temp_working_dir
    prob_json_filepath = os.path.join(prob_data_dir, "input_smoke_v1d00.json")
    submission_json_filepath = os.path.join(submissions_dir, "test_smoke_various", "test3_smoke.json")
    current_datetime = "2025-06-04-T05-05-05"
    str_current_datetime = str(current_datetime)
    result = validate_code_submission(str_current_datetime, prob_json_filepath, submission_json_filepath,
                                      temp_working_dir, output_dir, verbose)
    # In this case, check that this submission is invalid as "primary_method_name" is missing
    assert not result
