# -*- coding: utf-8 -*-
"""
test_linkedin.py

refs:
	https://github.com/DEKHTIARJonathan/python3-linkedin/blob/master/docs/index.md
	https://github.com/openstf/stf/issues/311
	https://github.com/requests/requests-oauthlib
	https://github.com/DEKHTIARJonathan/python3-linkedin/issues/4

2017-09-15

get keys from https://www.linkedin.com/secure/developer
    2017-09-15:
    client id = 863elc20vzc9aw
    client secret = W3QIy0zPt8uou0KE

API wrapper from https://github.com/DEKHTIARJonathan/python3-linkedin/
    pip install python3-linkedin
    
See "C:\Py_data\LinkedIn\python3-linkedin\examples" for 
    authentication.py
    http_api.py

Set LINKEDIN_API_KEY and LINKEDIN_API_SECRET, 
configure your app to redirect to http://localhost:8080/code.

HTTP API example
-----------------
    execute:
        http_api.py
    Visit http://localhost:8080 in your browser, curl or similar; 
        A tab in your browser will open up, give LinkedIn permission there
        You'll then be presented with a list of available routes, hit any, 
            e.g.: curl -XGET http://localhost:8080/get_profile

            
"""

# need to set conda env to 'prospecting'
#X: from linkedin import linkedin   
#E: from python3-linkedin import linkedin   
from linkedin import linkedin

 
"""
THIS IS PROBABLY USELESS::::::::::::::::
API_KEY = "wFNJekVpDCJtRPFX812pQsJee-gt0zO4X5XmG6wcfSOSlLocxodAXNMbl0_hw3Vl"
API_SECRET = "daJDa6_8UcnGMw1yuq9TjoO_PMKukXMo8vEMo7Qv5J-G3SPgrAV0FqFCd0TNjQyG"
RETURN_URL = "http://localhost:8000"
authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, 
                                                 linkedin.PERMISSIONS.enums.values())
print (authentication.authorization_url)
application = linkedin.LinkedInApplication(authentication)
"""

#-----------------------------------------------------------------------------
# http://thinktostart.com/download-your-linkedin-contacts-with-python/

"""
NFG??????????????????:::::::::::::::::
from https://pypi.python.org/pypi/python-linkedin ---
    use for debugging (KEY = 'wFNJekVpDCJtRPFX812pQsJee-gt0zO4X5XmG6wcfSOSlLocxodAXNMbl0_hw3Vl'
    SECRET = 'daJDa6_8UcnGMw1yuq9TjoO_PMKukXMo8vEMo7Qv5J-G3SPgrAV0FqFCd0TNjQyG'
    ==> WRONG: tokens valid 60 d
"""

"""
from https://pypi.python.org/pypi/python-linkedin ---

CONSUMER_KEY = 'XXX'
CONSUMER_SECRET = 'XXX'
USER_TOKEN = 'XXX'
USER_SECRET = 'XXX'
 
auth = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET,
                                                USER_TOKEN, USER_SECRET, RETURN_URL,
                                                permissions=linkedin.PERMISSIONS.enums.values())
 
app = linkedin.LinkedInApplication(auth)[/code]


# With the help of this app we can get our contacts with the get_connections() function. 
Then we store them in a JSON object.


[code language="python"]import json
connections = app.get_connections()
 
linkedin_contacts = 'contacts.json'
 
f = open(linkedin_contacts, 'w')
f.write(json.dumps(connections, indent=1))
f.close()


from prettytable import PrettyTable
pt = PrettyTable(field_names=['Name', 'Location'])
pt.align = 'l'
[pt.add_row((c['firstName'] + ' ' + c['lastName'], c['location']['name']))
for c in connections['values']
if c.has_key('location')]
print pt

"""

my_client_id = '863elc20vzc9aw'
my_client_secret = 'W3QIy0zPt8uou0KE'
my_redirect_uri = 'http://localhost:8080/code'
#my_redirect_uri = 'http://127.0.0.1:8080/code'
# untested: my_redirect_uri = 'http://127.0.0.1:8080'

# http://requests-oauthlib.readthedocs.io/en/latest/examples/linkedin.html

# OAuth endpoints given in the LinkedIn API documentation:
authorization_base_url = 'https://www.linkedin.com/uas/oauth2/authorization'
token_url = 'https://www.linkedin.com/uas/oauth2/accessToken'

from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import linkedin_compliance_fix

#linkedin = OAuth2Session(my_client_id, redirect_uri='http://127.0.0.1')
linkedin = OAuth2Session(my_client_id, redirect_uri=my_redirect_uri)
linkedin = linkedin_compliance_fix(linkedin)

# Redirect user to LinkedIn for authorization
authorization_url, state = linkedin.authorization_url(authorization_base_url)
print ('Please go here and authorize: {}'.format(authorization_url))

# Get the authorization verifier code from the callback url
redirect_response = input('Paste the full redirect URL here:')

# Fetch the access token
linkedin.fetch_token(token_url, client_secret=my_client_secret, 
                     authorization_response=redirect_response)

# Fetch a protected resource, i.e. user profile
r = linkedin.get('https://api.linkedin.com/v1/people/~')
print (r.content)

