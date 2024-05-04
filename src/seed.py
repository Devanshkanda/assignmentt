import csv

cached_bank_ids_and_names = dict()

def get_bank_names_and_ids() -> dict | None:
    try:
        with open("../bank_branches.csv", "r") as file:
            readcsv = csv.reader(file)
            bank_ids_and_names = dict()

            for line in readcsv:
                if not line[1] in bank_ids_and_names.keys():
                    bank_ids_and_names[line[1]] = line[7]
                else:
                    continue
            
            cached_bank_ids_and_names = bank_ids_and_names.copy()
            # print(cached_bank_ids_and_names)
            return bank_ids_and_names
        
    except Exception as e:
        print(f"Error while fetching bank ids and names from csv file: {e}")
        return None


def get_branch_details(ifsc_code: str) -> list | None:
    try:
        with open("../bank_branches.csv", "r") as file:
            readcsv = csv.reader(file)
        
            for line in readcsv:
                if ifsc_code in line:
                    return line
            
            return None

    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    get_bank_names_and_ids()