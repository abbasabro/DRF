import csv

def handleExcelUpload(file_path):
    try:
        with open(file_path,"r") as file:
            reader = csv.DictReader(file)
    except Exception as e:
        print(e)