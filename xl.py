from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime
import re
from gspread.exceptions import APIError, WorksheetNotFound

GOOGLE_SERVICE_ACCOUNT_JSON_PATH = "static/Google_sheet_upload_POCI.json"
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1wk47WfmTuab0SKbGZqTTISUhT55lTuopmSnqJaiQ1VE/edit?usp=sharing"

def update_google_sheet(name, email, password, blog_url, landing_page, blog_tags, name_type="Blog Post", status="DONE", sheet_name="Blog_Posts"):
    """Updates Google Sheet with blog upload details."""
    try:
        print(f"📝 Updating sheet: {sheet_name}")

        # Clean inputs
        sheet_name = re.sub(r'[^\w\s-]', '', sheet_name).strip().replace(' ', '_')
        blog_tags = blog_tags.strip().replace('\n', ', ')

        # Authenticate
        print("Authenticating with Google Sheets...")
        creds = Credentials.from_service_account_file(
            GOOGLE_SERVICE_ACCOUNT_JSON_PATH,
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        client = gspread.authorize(creds)
        
        print("Opening spreadsheet...")
        try:
            spreadsheet = client.open_by_url(GOOGLE_SHEET_URL)
            print("Spreadsheet opened successfully")
        except Exception as e:
            print(f"❌ Failed to open spreadsheet: {e}")
            return False

        # Worksheet handling
        print(f"Accessing worksheet '{sheet_name}'...")
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
            print("Worksheet found")
        except WorksheetNotFound:
            print("Worksheet not found, creating new one...")
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=20)
            headers = ["Date", "Name", "Email", "Password", "Blog URL", "Landing Page", "Tags", "Type", "Status"]
            worksheet.append_row(headers)
            print("New worksheet created with headers")
        
        # Prepare data
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row_data = [
            current_date,
            name,
            email,
            password,
            blog_url,
            landing_page,
            blog_tags,
            name_type,
            status
        ]
        
        print("Appending row:", row_data)
        worksheet.append_row(row_data)
        print(f"✅ Data successfully added to sheet: '{sheet_name}'")
        return True
        
    except APIError as e:
        print(f"❌ Google Sheets API Error: {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {type(e).__name__} - {str(e)}")
        return False