

import requests

# מפתח ה-API שלך מ-VirusTotal
api_key = '455285bbe8097f33a012ca820b02a41f5d442529de887ad163294d1c098fd769'

# הנתיב לקובץ שאתה רוצה לסרוק
file_path = r'C:\איתן\EitanWebApplication\EitanWebApplication\App_Data\Database1.mdf'

# שליחת הקובץ ל-VirusTotal לסריקה
url = 'https://www.virustotal.com/vtapi/v2/file/scan'
files = {'file': (file_path, open(file_path, 'rb'))}
params = {'apikey': api_key}
response = requests.post(url, files=files, params=params)
scan_id = response.json().get('scan_id')

if scan_id:
    print(f"File uploaded successfully. Scan ID: {scan_id}")
else:
    print("Error uploading file.")
    exit()

# קבלת התוצאות של הסריקה
report_url = 'https://www.virustotal.com/vtapi/v2/file/report'
params = {'apikey': api_key, 'resource': scan_id}
response = requests.get(report_url, params=params)
report = response.json()

# בדיקת תוצאות הסריקה
if report.get('response_code') == 1:
    print(f"Scan Report:\n"
          f"Positives: {report.get('positives')}\n"
          f"Total: {report.get('total')}\n"
          f"Scan Date: {report.get('scan_date')}\n")
    print("Detailed report:")
    for antivirus, data in report.get('scans', {}).items():
        print(f"{antivirus}: {data['result']}")
else:
    print("No report found for the provided scan ID.")

