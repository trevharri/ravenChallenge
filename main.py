import json, re
from collections import defaultdict
TEST_PATH = "/Users/trevorharrington/Documents/ravenChallenge/rt-feed-record"


def process_json_lines(file_path):
    lines_by_document_id = defaultdict(list)

    with open(file_path, "r") as f:
            data = f.readlines()
            for line in data:
                line = json.loads(line.strip())
                lines_by_document_id[line["RP_DOCUMENT_ID"]].append(line)

    return lines_by_document_id


def check_for_missing_records(lines_by_document_id):
    missing_data = []
    unique_ids = set(lines_by_document_id.keys())

    for document_id in unique_ids:
        expected_record_count = lines_by_document_id[document_id][0]["DOCUMENT_RECORD_COUNT"]
        expected_indices = set(range(1, expected_record_count + 1))
        actual_entries = lines_by_document_id[document_id]


        for entry in actual_entries:
            if entry["DOCUMENT_RECORD_INDEX"] in expected_indices:
                expected_indices.remove(entry["DOCUMENT_RECORD_INDEX"])

        if expected_indices:
            missing_data.append({"id": document_id, "missing_documents": list(expected_indices)})
    if len(missing_data) > 0:
        return missing_data
    else:
        return False

def validate_rp_entity_id(id_string):
    id_string = id_string
    if not isinstance(id_string, unicode):
        return False

    pattern = r'^[A-Z0-9]{6}$'

    return bool(re.match(pattern, id_string))

processed_data = process_json_lines(TEST_PATH)
missing_data = check_for_missing_records(processed_data)

print(len(set(processed_data.keys())))
print(missing_data)
print(validate_rp_entity_id(u"46Ee13"))