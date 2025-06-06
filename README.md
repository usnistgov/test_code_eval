# README.md

This describes the repository "test_code_eval", which is a pilot experiment to
test if AI-Generated Code can be used to help test software. This experiment
also doubles as an infrastructure.

This code contains the genai_code_test package. Full documentation of the `genai_code_test` package is on
the [genai_code_test gitlab pages](https://genai_code.ipages.nist.gov/test_code_eval/).

The test cases include some sample data that can be used to explore this package. However, this repository only 
stores the software code and does not store the data.

## Contact

For specific software questions, please contace Peter Fontana <peter.fontana@nist.gov>. For questions
related to the NIST Generative AI (GenAI) Program, please contact <genai_poc@nist.gov>

## Contributors

The contributors to this code repository are:

* Peter Fontana <peter.fontana@nist.gov>
* Sonika Sharma <sonika.sharma@nist.gov>

## Environment Variables and Configuration

The majority of configurations will be provided in a `.ini` file. The typical default file,
`config.ini` is provided as an example. `config_ci.ini` is a special configuration file used for Continuous 
Integration (CI) purposes.

Additionally, this program uses one environment variables for convenience:

```bash
GENAI_CODE_CONFIG_PATH
```

`GENAI_CODE_CONFIG_PATH` is the absolute path to the default config file, which may be 
the `config.ini` file. Within the configuration file, is the variable `repo_dir`, which provides the absolute path 
to this repository directory.

Additionally, for convenience, we store the root path to this repository in the environment variable

```bash
GENAI_CODE_REPO_DIR
```

## Code Installation

The code is tested on python 3.12.6 and is pip installable with:

```bash
pip install .
```

or can be installed in editable mode with:

```bash
pip install -e .
```

The package installed is named `genai_code_test`. The package can be uninstalled with:

```bash
pip uninstall genai_code_test
```

or uninstalled if installed in editable mode with:

```bash
rm -r genai_code_test.egg-info
pip uninstall genai_code_test
````


## Organizational Structure

The organization structure of folders is here. There is also this README.md, and a CHANGELOG.md.

    test_code_eval (<root directory of repository referred to as $GENAI_CODE_REPO_DIR in this README.md>)
        - docs (pre-built documentation)
        - genai_code_test (root code director for python code for genai code experiment and evaluation)
            - baseline_system_creation (scripts to create human-generated baseline submissions from
              code bank files)
            - evaluation_environment (directory with scorer and validator)
                - evaluate_submission.py (the scorer)
                - validate_submission.py (the validator)
            - utils (utility scripts helpful for ease of working with json submissions and creating data files.
              Relevant scripts include)
                - create_code_files_from_json_input.py (Takes a validly-formatted json submission and converts
                  it to a folder of folders and files to allow for human-readable viewing of the code strings
                  as files)
                - create_json_files_from_code_files.py (Takes a folder of folders and files and converts to a 
                  json submission. Useful to use when one converted a json using the 
                  create_code_files_from_json_input.py script to folders and then modified the files in that folder.
                  This allows one to convert it back to a json.)
                - extract_test_code_from_test_output.json (The tool we used to extract validly formatted test_code
                  from LLM outpus. This converts LLM output when LLMs followed our prompt instructions but this script
                  will not handle arbitrary LLM output.)
        - test_data (directory with test data for test cases)
        - test_working_space (working directory where test cases create temporary working files and produce
          output files)
        - tests (location of test suite code)

For an example submission, look at the file 
[test_data/submissions_test/test_smoke_various/test1_v0d99_smoke.json](test_data/submissions_test/test_smoke_various/test1_v0d99_smoke.json)


 ## Running the Scorer and Validator
The scripts `evaluate_submission.py` and `validate_submission.py` are command-line scripts and their help menu
can be accessed with

```bash
python evaluate_submission.py -h
```

and 

```bash
python validate_submission.py -h
```

If you are in teh directory `$GENAI_CODE_REPO_DIR/genai_code_test/evaluation_environment`, the script to validate the
example test submission is

```bash
python validate_submission.py -i $GENAI_CODE_REPO_DIR/test_data/code_files_test/prob_data/input_smoke_v1d00.json -o $GENAI_CODE_REPO_DIR/scratch_output/evaluation -w $GENAI_CODE_REPO_DIR/scratch_working_space -s $GENAI_CODE_REPO_DIR/test_data/submissions_test/test_smoke_various/test1_v0d99_smoke.json -v```
```

and the script to score the test submission is:

```bash
python evaluate_submission.py -k $GENAI_CODE_REPO_DIR/test_data/code_files_test/key_data/key_smoke_v1d00.json -o $GENAI_CODE_REPO_DIR/scratch_output/evaluation -w $GENAI_CODE_REPO_DIR/scratch_working_space -s $GENAI_CODE_REPO_DIR/test_data/submissions_test/test_smoke_various/test1_v0d99_smoke.json
```

In both of these scripts, we provide a working directory with `-w <working_dir_path>` where the code can both
write temporary files and delete any files in those directories. We also specified the output with `-o output_dir_path`

**Both `validate_submission.py` and `evaluate_submission.py` may remove all files in the working directory specified by 
`-w <working_dir_path>`.  Please provide `-w` with an *empty* directory where the code can create and delete files.**


## Running Continuous Integration Components Locally

The Continuous Integration (CI) runs the test suite, generates rendered API documentation, and also checks the code for
formatting using a lint code tool. These components can all be run locally, and instructions
are below.

### Testing

We have a test suite with the `pytest` package and code coverage with `coverage`. This requires the package `coverage` 
and `pytest`, both of which can be installed with `pip`.

The following command runs all the unit tests and outputs code coverage into `htmlcov/index.html`

```bash
coverage run --branch --source=./genai_code_test -m pytest -s tests/ -v
coverage report -m
coverage html
```

**When running the tests, there is a fixture defined in `/tests/conftest.py` that removes all of the files in `test_working_space/temp_working_space`
and `test_working_space/temp_output`**

### Code Formatting

The CI uses `flake8` to check for the code formatting with the command

```bash
flake8 --extend-ignore=E712,E402 genai_code_test tests --max-line-length=120 --exclude=docs,./.* 
```

For automatic styling, we will use the `autopep8` package. To style the code, use

```bash
autopep8  --max-line-length 120 --aggressive --aggressive  --ignore E226,E24,W50,W690,E712,E402 -r genai_code_test tests --in-place
```

If you wish to see what the changes are without making them use the `--diff` option with

```bash
autopep8  --max-line-length 120 --aggressive --aggressive  --ignore E226,E24,W50,W690,E712,E402 -r genai_code_test tests --diff
```

### Documentation

To build the documentation with `sphinx` and `autodoc`, run

```bash
# A Pip installation may be necessary to generate the docs. Install the package with:
# pip install -U -e .
sphinx-apidoc -fMeT -o docs/api genai_code_test
sphinx-build -av --color -b html docs docs/_build
```

to generate the docs. The pip install command is needed for sphinx to recognize the `genai_code_test` module.

(If you wish to document what is installed by pip, use the commented line to upgrade PIP)

See the [Sphinx Installation Documentation](https://www.sphinx-doc.org/en/master/usage/installation.html) 
for more information on how to install Sphinx. You will also need the `m2r` package which is a requirement of this  
package.

We are using Sphinx 7.
