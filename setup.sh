
#!/bin/bash

# clean-up directories if they already exist
rm -fdr venv

# create a virtual environment
python3 -m venv venv

# activate it
source pwbvenv/bin/activate

# install dependencies
pip install -r requirements.txt