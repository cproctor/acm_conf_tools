# ACM Conference Tools

This repository contains Python utilities related to ACM conference proceedings 
which I never want to do again by hand. Currently, utilities are provided for 
extracting submission information from EasyChair and converting it into the 
bizarre CSV format required for ACM rights notifications. 

To do this:

0. Install required packages via `pip install -r requirements.txt` (ideally into 
   a virtual env).
1. Create secrets.yaml with the following keys. Obviously, you will need
   appropriate privileges in EasyChair
    - CONFERENCE_ID (Look in the Easy Chair URL query params)
    - EASY_CHAIR_USERNAME
    - EASY_CHAIR_PASSWORD
2. Run `scraper.py`.
3. Run `convert_csv.py`. You might need to tweak this script for your
   conference's settings.
4. The result is `submissions_for_acm.csv`.
