import smartsheet

# Instantiate smartsheet and specify access token value.
# smartsheet = smartsheet.Smartsheet('ACCESS_TOKEN')
# Get Id of the Sheet
# https://support.klipfolio.com/hc/en-us/articles/215546768-Creating-a-Smartsheet-data-source

smartsheet = smartsheet.Smartsheet('ACCESS_TOKEN')

SHEET_ID = '9999999999'

sSheet = smartsheet.Sheets.get_sheet(SHEET_ID) #, column_ids=columnlist
for row in sSheet.rows:
    if row.row_number == 4:
        for col in range(0, len(sSheet.columns)):
            print(row.cells[col].value)
