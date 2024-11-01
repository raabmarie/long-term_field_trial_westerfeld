import openpyxl
import os
from openpyxl import load_workbook

path = "Datenstruktur/Nmin/Nmin_3"

for file_name in os.listdir(path):
    if file_name.endswith(".xlsx"):
        # Open Excel file
        workbook = load_workbook(os.path.join(path, file_name))
        # Iterate through all tabs
        for worksheet in workbook.worksheets:
            if worksheet.title.strip() in ["NFK1", "NFK2", "Nmin Ernte", "Nmin Frühj"]:
                worksheet.title = worksheet.title.strip()

        # Save file
        workbook.save(file_name)

print("done")
