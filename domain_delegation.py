#!/usr/bin/python
# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Simple program to demonstrate the Google+ Domains API.

This program shows how to authenticate an app for domain-wide delegation and how
to complete an activities.insert API call. For details on how to authenticate on
a per-user basis using OAuth 2.0, or for examples of other API calls, please see
the documentation at https://developers.google.com/+/domains/.

Changelog:
- 2017-12-29: 
--- Update authenticate() to use JSON credentials.
--- Remove SERVICE_ACCOUNT_EMAIL, as it's not necessary for JSON authentication.
--- Replace references to SERVICE_ACCOUNT_PKCS12_FILE_PATH with SERVICE_ACCOUNT_JSON_FILE_PATH, and update the associated path.
"""

__author__ = 'joannasmith@google.com (Joanna Smith)'

import httplib2
import pprint

from apiclient.discovery import build

from oauth2client.service_account import ServiceAccountCredentials

#--- Start remove section.
# Update SERVICE_ACCOUNT_PKCS12_FILE_PATH with the file path to the private key
# file downloaded from the developer console.
SERVICE_ACCOUNT_PKCS12_FILE_PATH = '/path/to/<public_key_fingerprint>-privatekey.p12'
#--- End remove section.

#--- Start add section.
# Update SERVICE_ACCOUNT_JSON_FILE_PATH with the file path to the private key
# file downloaded from the developer console.
SERVICE_ACCOUNT_JSON_FILE_PATH = '/path/to/<private-key>.json'
#--- End add section.

# Update USER_EMAIL with the email address of the user within your domain that
# you would like to act on behalf of.
USER_EMAIL = 'user@mydomain.com'

# plus.me and plus.stream.write are the scopes required to perform the tasks in
# this quickstart. For a full list of available scopes and their uses, please
# see the documentation.
SCOPES = ['https://www.googleapis.com/auth/plus.me',
          'https://www.googleapis.com/auth/plus.stream.write']


def authenticate():
  """Build and return a Plus service object authorized with the service accounts
  that act on behalf of the given user.

  Returns:
    Plus service object.
  """

  print 'Authenticate the domain for %s' % USER_EMAIL

  # Make service account credentials
  #--- Replace this line.
  credentials = ServiceAccountCredentials.from_p12_keyfile(
    SERVICE_ACCOUNT_EMAIL, SERVICE_ACCOUNT_PKCS12_FILE_PATH, scopes=SCOPES)
  #--- With this line.
  credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_JSON_FILE_PATH, scopes=SCOPES)

  # Setting the sub field with USER_EMAIL allows you to make API calls using the
  # special keyword 'me' in place of a user id for that user.
  delegate_credentials = credentials.create_delegated(USER_EMAIL)

  http = httplib2.Http()
  http = delegate_credentials.authorize(http)

  # Create and return the Plus service object
  return build('plusDomains', 'v1', http=http)


def activitiesInsert(service):
  """Create a new post on behalf of the given user, restricted to the domain.

  Args:
    service: the Plus service object.
  """

  # Set the user's ID to 'me': requires the plus.me scope
  user_id = 'me'

  # Insert an Activity
  print 'Inserting activity'
  result = service.activities().insert(
      userId = user_id,
      body = {
          'object' : {
              'originalContent' : 'Happy Monday! #caseofthemondays'
          },
          'access' : {
              'items' : [{
                  'type' : 'domain'
              }],
              # Required, this does the domain restriction
              'domainRestricted': True
          }
      }).execute()
  print 'result = %s' % pprint.pformat(result)


if __name__ == '__main__':
  service = authenticate()
  activitiesInsert(service)

