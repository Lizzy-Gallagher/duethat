from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
from CalItem import CalItem

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

class GoogleCalendar(object):
    def __init__(self):
        self.service = self._get_service()

    # Use this function
    def send_to_google_calendar(self, cal_item):
        event = self._create_event(cal_item)
        event = self.service.events().insert(calendarId='primary', body=event).execute()
        print ('Event created: %s' % (event.get('htmlLink')))

    def _get_service(self):
        credentials = self._get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        return service

    def _get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    # Creates an event ready for Google Calendar
    def _create_event(self, cal_item):
        end_time = "2016-02-28T11:00:00-00:00"

        event = {
          'summary': cal_item.create_description(),
          'location': cal_item.location,
          'description': cal_item.create_description(),
          'start': {
            'dateTime': cal_item.start_time,
            'timeZone': 'America/Los_Angeles',
          },
          'end': {
            'dateTime': end_time,
            'timeZone': 'America/Los_Angeles',
          },
          'reminders': {
            'useDefault': True
          }
        }
        return event

# Sample Usage of this Object
def sample():
        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        google_calendar = GoogleCalendar()

        action = "Go to  "
        action_target = "Fellowship Meeting"
        location = "Green Hall"
        start_time = "2016-02-28T09:00:00-00:00"

        cal_item = CalItem(action, action_target, location, start_time)
        google_calendar.send_to_google_calendar(cal_item)

if __name__ == '__main__':
    sample()
