from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

from TaskItem import TaskItem

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/tasks-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/tasks'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Tasks API Python Quickstart'

class GoogleTask(object):
    def __init__(self):
        self.service = self._get_service()

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
                                       'tasks-python-quickstart.json')

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

    def _get_service(self):
        credentials = self._get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('tasks', 'v1', http=http)
        return service

    def add_task(self, task):
        if task.due_date == "":
            task.due_date = '2016-2-29T12:00:00.000Z'
        if task.location == "":
            task = {
                'title': task.create_title(),
                'notes': task.query,
                'due': task.due_date
            }
            self.service.tasks().insert(tasklist='@default', body=task).execute()
        else:
            task = {
                'title': task.create_title(),
                'notes': task.query,
                'due': task.due_date
            }
            self.service.tasks().insert(tasklist='@default', body=task).execute()
        # print (task.items())



    # Depreciated, kept for posterity
    def _list_task_lists(self):
        results = self.service.tasklists().list(maxResults=10).execute()
        items = results.get('items', [])
        if not items:
            print('No task lists found.')
        else:
            print('Task lists:')
            for item in items:
                print('{0} ({1})'.format(item['title'], item['id']))

def sample():
    """Shows basic usage of the Google Tasks API.

    Creates a Google Tasks API service object and outputs the first 10
    task lists.
    """
    google_task = GoogleTask()

    task = TaskItem('Action2', 'Action Target', 'Place', '2010-10-15T12:00:00.000Z')
    google_task.add_task(task)

if __name__ == '__main__':
    sample()
