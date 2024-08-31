# ravenChallenge
This repository contains a simple application that can be used to read a jsonlines file and validate its information


====================
# Quick Start Guide:
## without Docker
1. Unpack .rar file and add document containing jsonlines to the `ravenChallenge/data` directory
2. Open a terminal in the `ravenChallenge` directory
3. Run the command `python3 main.py`, type the name of your data file (the one you've added to `/data`) and hit enter.
4. Follow the instructions in the terminal to view/validate data
## Docker
1. Unpack .rar file in a directory of your choice
2. Copy the file path of the directory you choose
3. Pull the `trevorRavenChallenge` docker image from docker hub
4. Run a docker container from that image and attach your data file directory using the command:
`docker run -ti  -v /YOUR_COPIED_DIRECTORY_PATH:/data trevorRavenChallenge`
5. Type the name of your data file (the one in`/YOUR_COPIED_DIRECTORY_PATH`)
6. Follow the instructions in the terminal to view/validate data

====================
# Project Structure
The project has the following structure:

- `ravenChallenge/`: Contains all project files.
  - `data/`: Is an empty directory. We will mount and external datafile here when we run the docker container.
  - `FeedData.py`: Has the FeedData class which contains all the methods for reading/processing our data.
  - `main.py`: Our main app file contains a simple cmd line app.
  - `Dockerfile`: Simple docker file creating docker image from code.


====================
# FeedData
## Description:
------------
This class contains the bulk of our data validating logic.

Upon initialization the `process_json_lines` method is called. This reads the data file line-by-line, deletes white spaces and then reorganizes the data into a dictionary where the keys are RP_DOCUMENT_IDs and the values are lists containing every line for that RP_DOCUMENT_ID.
`{RP_DOCUMENT_ID1: [line1, line2 line3, ...], RP_DOCUMENT_ID2: [line1, line2, line3 ...], ...}`
This is stored in the `lines_by_document_id` attribute. There is error handling to make sure the document exists, is readable, each line is json format and each line has the RP_DOCUMENT_ID key.

The `distinct_stories` attribute sums the keys from `lines_by_document_id` to get a count of the unique documents.

The `check_for_missing_records` method takes our `lines_by_document_id` dictionary, gets the keys and then iterates through each of them checking that there are records for every DOCUMENT_RECORD_INDEX in the DOCUMENT_RECORD_COUNT. To do this a set is created for each index in DOCUMENT_RECORD_INDEX. As we iterate through finding the records, thier indexes are removed from that set. After iterating through the set, if any missing indexs remain. The indexes and their respective document id are added to list which the method returns

The `is_valid_rp_entity_id` method checks if the value of an RP_ENTITY_ID is valid. To do the method check that the value is a string and then uses a regex expression to validate that it is 6 characters in length and contains only capital letters and integers. If the id is valid, then method returns true.

The `validate_entity_ids_by_document` method takes a RP_DOCUMENT_ID and iterates through all associated entity ids using `is_valid_rp_entity_id` to validate the ids. If invalid ids are found, they are added to a list that is returned by the method.


====================
# Possible improvements:
------
- Use library like unrar to automate the to unzipping of the .rar file.
- Add feature to generate html reports about the findings.
- Improve error handling
- Investigate better datastructures to make app run faster with large files.
- Organize prompts from main.py into separate file for better readability.


