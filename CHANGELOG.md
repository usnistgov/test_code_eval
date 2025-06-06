# CHANGELOG.md

## v2024.06.05

Updated code to work with pilot evaluation version 1.0 and to automate workflows.

Significant changes:
* Change in code bank format
* Change in submission json format
* Updated Test case
* Additional Utility scripts useful for making code banks and for producing baseline system results.
* Updated documentation
* a variety of bugfixes

## v2024.10.14_dev

Updated code to work for the pilot evaluation and reorganized code

Significant Changes:
* Separated out evaluator data from the code
* Updated json field names of all data files to work with the pilot evaluation
* Developed a code_bank_file that is manually produced to contain the code bank.
* From the code_bank_file, developed automated scripts to produce the key files and problem input files
as formatted for the pilot
* Created a public smoke_test code bank for testing and validation
* Wrote the validator validate_submission.py

## v2024.10.03_dev

First version of code package that reorganizes and runs the code for the preliminary experiment.