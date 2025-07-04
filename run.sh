#!/bin/bash

# clean up plans.db
FILE_TO_DELETE="./python-backend/roaming_plans.db"
if [ -f "$FILE_TO_DELETE" ]; then
  echo "'$FILE_TO_DELETE' found. Deleting for clean install."
  rm "$FILE_TO_DELETE"

  # Check the exit status of the rm command
  if [ $? -eq 0 ]; then
    echo "Successfully deleted '$FILE_TO_DELETE'."
  else
    echo "Error: Failed to delete '$FILE_TO_DELETE'."
  fi
else
  echo "'$FILE_TO_DELETE' does not exist or is not a regular file. No action taken."
fi

# setup necessary stuff
pip install -r ./python-backend/requirements.txt # install requirements
python3 ./python-backend/utils/build_plans_db.py $FILE_TO_DELETE # recreate clean plans.db; take note of relative pathing

# run ui
npm --prefix ./ui install
npm --prefix ./ui run dev

