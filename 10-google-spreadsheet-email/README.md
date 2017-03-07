# Sending Email reading Input from a Google Spreadsheet

## Usage:

```
./gen_letters "spreadsheet name" template_name
```

The JSON containing the credentials is greated using Google´s Developer Console. The spreadsheet has to be shared with the service account email listed in the JSON file, otherwise an SpreadsheetNotFound exception will be thrown.

## Dependencies:

The following python modules are needed (all are available via pip):

```
pyopenssl
gspread
oauth2client (1.5.2)
```

In particular, oauth2client has to be version 1.5.2. use this form of pip to force:

```
 pip install oauth2client==1.5.2
```
