"""
Danger Will Robinson.
"""

from documentcloud.addon import AddOn
import gspread
import re, os
from datetime import datetime
import csv


"""
  spreadsheet:
    # The URL of a Google Sheet you want to bulk file with.
    title: Google Sheet URL
    type: string
  api_key:
    # Your MuckRock API key. Not currently actually used.
    title: MuckRock API Key
    type: string
  google_client_id:
    title: Google Client ID
    type: string
  google_project_id:
    title: Google Project ID
    type: string
  google_secret_id:
    title: Google Client Secret
    type: string
"""

class BulkFile(AddOn):

    def main(self):
        """The main add-on functionality goes here."""
        # fetch your add-on specific data
        print("got this far")
        credentials = {
                "installed": {
                "client_id": self.data.get("google_client_id"),
                "project_id": self.data.get("google_project_id"),
                "auth_uri":"https://accounts.google.com/o/oauth2/auth",
                "token_uri":"https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
                "client_secret":self.data.get("google_secret_id"),
                "redirect_uris":"http://localhost"
                }
        }
        print("Credentials locked and loaded."
        gc, authorized_user = gspread.oauth_from_dict(credentials)

        row = 2 # skip the first row, which is reserved for headers
        worksheet = 0 # worksheets are 0-indexed
        spreadsheet = self.data.get("spreadsheet")
        
        print("Opening the spreadsheet %s..."%spreadsheet)
        self.set_message("Opening the spreadsheet %s..."%spreadsheet)
        
        muckrock_api_key = self.data.get("api_key")

        url = 'https://www.muckrock.com/api_v1/'
        headers = {
        'Authorization': 'Token %s' % token,
        'content-type': 'application/json'
        }
                            
                             
        try:
            if spreadsheet.startswith("http"):
                self.set_message("Opening spreadsheet by url...")
                ht1 = gc.open_by_url(spreadsheet).get_worksheet(worksheet)
            else: # Try to open it just by name
                sht1 = gc.open(spreadsheet).get_worksheet(worksheet)
        except:
            self.set_message("Couldn't open the spreadsheet. Check the url and try again.")
            return
        while True:
          print("Checking row %s..."%row)
          self.set_message("Checking row %s..."%row)
          try:
              agency = sht1.cell(row, 1).value
              print(agency)
              if agency == "" or agency == None:
                  print("No agency at row %s, terminating run here."%row)
                  self.set_message("No agency at row %s, terminating run here."%row)
                  break
              else:
                  if sht1.cell(row, 4).value == None or sht1.cell(row, 4).value == "": # Check Filed Status
                      try:
                          data = json.dumps({
                              'agency': sht1.cell(row, 1).value,
                              'title': sht1.cell(row, 3).value,
                              'full_text': sht1.cell(row, 2).value,
                      #        'attachments': [attachment],
                      #         'embargo': True
                              'permanent_embargo': True
                          })

                      # The request will be saved as a draft if you do not have any requests left
                          r = requests.post(url + 'foia/', headers=headers, data=data)
                          sht1.update_cell(row, 4, "Filed Succesully")
                          print(r)
                          row += 1
                      except:
                          row += 1 # Probbly don't need a break after this.
                          break
          except:
              break



if __name__ == "__main__":
    BulkFile().main()
