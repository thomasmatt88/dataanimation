from openpyxl import load_workbook
import re

def creationdate(file_path):
    
    wb = load_workbook(file_path) #unknown extension warning
    wbcreation_date = str(wb.properties.created) #turn 'created' into str from datetime object

    return wbcreation_date
# InvalidFileException: openpyxl does not support the old .xls file format,
#please use xlrd to read this file, or convert it to the more recent .xlsx file format.

