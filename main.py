from FeedData import FeedData
import os


file_name = input("Please enter the name of you data file: ")
feed_data = FeedData(f"./data/{file_name}")

turn_off = False
while not turn_off:
    print(f"\nYour data file contains {feed_data.distinct_stories} distinct stories(RP_DOCUMENT_IDS).\n")
    print("Select an option: ")
    print("[1] View list of all unique RP_DOCUMENT_IDs")
    print("[2] Check for stories with missing records")
    print("[3] Validate individual RP_ENTITY_ID")
    print('[4] Validate all RP_ENTITY_IDs for given document')
    print("[5] Exit")
    user_choice = input("\nPlease type a number 1-5 and hit enter: ")

    if str(user_choice) == "5":
        break

    elif user_choice == "1":
        for id in feed_data.lines_by_document_id.keys():
            print(id)

    elif user_choice == "2":
        missing_records = feed_data.check_for_missing_records()
        if missing_records:
            for document in missing_records:
                print(f'\nDocument {document["id"]} is missing records with index(s) {document["missing_documents"]}')
        else:
            print("No documents are missing records")

    elif user_choice == "3":
        entity_id = input("Please type the entity id and hit enter: ")
        is_valid = feed_data.is_valid_rp_entity_id(entity_id)
        if is_valid:
            print("ID is valid")
        else:
            print("Id is invalid")

    elif user_choice == "4":
        document_id = input("Please type document id and hit enter: ")
        invalid_ids = feed_data.validate_entity_ids_by_document(document_id)
        if invalid_ids:
            print(f"The following ids are invalid: {invalid_ids}")
        else:
            print("All ids are valid")

    user_continues = input("\nWould you like to continue? [y/n]: ")
    if user_continues == "y":
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        turn_off = True
        print("Goodbye!")
