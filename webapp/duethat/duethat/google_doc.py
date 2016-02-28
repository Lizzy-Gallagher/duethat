from __future__ import print_function
import httplib2
import os

import io

import textract
from apiclient import discovery
from apiclient import errors
from apiclient.http import MediaIoBaseDownload
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

# If modifying these scopes, delete your previously saved credentials
# at ./.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

def get_credentials():
	"""Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
	credential_dir = '.credentials'
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,
								   'drive-python-quickstart.json')

	store = oauth2client.file.Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else:  # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

def download_file(filename, item, service):
	"""Downloads item to filename."""
	id = item['id']
	request = service.files().export_media(fileId=id,
										   mimeType='application/pdf')
	fh = io.BytesIO()
	downloader = MediaIoBaseDownload(fh, request)
	done = False
	while done is False:
		status, done = downloader.next_chunk()
	open(filename, 'wb').write(fh.getvalue())

def list_files(service):
	"""Retrieve a list of File resources.

	Args:
	  service: Drive API service instance.
	Returns:
	  List of File resources.
	"""
	temp_result = []
	page_token = None
	while True:
		try:
			param = {}
			if page_token:
				param['pageToken'] = page_token
			files = service.files().list(**param).execute()

			temp_result.extend(files['files'])
			page_token = files.get('nextPageToken')
			if not page_token:
				break
		except errors.HttpError, error:
			print
			'An error occurred: %s' % error
			break

	result = []

	for res in temp_result:
		if res['mimeType'] == 'application/vnd.google-apps.document':
			result.append(res)

	return result

def main():
	"""Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('drive', 'v3', http=http)

	available_files = list_files(service)
	last_item = available_files[0]
	filename = last_item['id'] + '.pdf'
	download_file(filename, last_item, service)
	text = textract.process(filename)
	return text

if __name__ == '__main__':
	print (main()) # returns the text from the first file
