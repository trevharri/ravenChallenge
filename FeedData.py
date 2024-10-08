import json
import re
from collections import defaultdict


class FeedData:

    def __init__(self, file_path):
        self.lines_by_document_id = self.process_json_lines(file_path)
        self.distinct_stories = len(self.lines_by_document_id.keys())

    def process_json_lines(self, file_path):
        lines_by_document_id = defaultdict(list)
        try:
            with open(file_path, "r") as f:
                try:
                    data = f.readlines()
                    count = 1
                    for line in data:
                        try:
                            line = json.loads(line.strip())
                            document_id = line["RP_DOCUMENT_ID"]
                            lines_by_document_id[document_id].append(line)
                            count += 1
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON in line: {count}  -- Line not processed")
                        except KeyError as e:
                            print(f"Missing key {e} in line: {count} -- Line not processed")
                except Exception as e:
                    print(f"An error occurred while reading the file: {e}")
        except FileNotFoundError:
            print(f"The file {file_path} does not exist.")
        except IOError as e:
            print(f"An I/O error occurred: {e}")
        return lines_by_document_id

    def check_for_missing_records(self):
        missing_data = []
        unique_ids = set(self.lines_by_document_id.keys())

        for document_id in unique_ids:
            expected_record_count = self.lines_by_document_id[document_id][0]["DOCUMENT_RECORD_COUNT"]
            expected_indices = set(range(1, expected_record_count + 1))
            actual_entries = self.lines_by_document_id[document_id]

            for entry in actual_entries:
                if entry["DOCUMENT_RECORD_INDEX"] in expected_indices:
                    expected_indices.remove(entry["DOCUMENT_RECORD_INDEX"])

            if expected_indices:
                missing_data.append({"id": document_id, "missing_documents": list(expected_indices)})

        if len(missing_data) > 0:
            return missing_data
        else:
            return False

    def is_valid_rp_entity_id(self, id_string):
        if not isinstance(id_string, str):
            return False

        pattern = r'^[A-Z0-9]{6}$'

        return bool(re.match(pattern, id_string))

    def validate_entity_ids_by_document(self, document_id):
        invalid_entities = []
        entities = self.lines_by_document_id[document_id]

        for entity in entities:
            if not self.is_valid_rp_entity_id(entity["RP_ENTITY_ID"]):
                invalid_entities.append(entity["RP_ENTITY_ID"])

        return invalid_entities
