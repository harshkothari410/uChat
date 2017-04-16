from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.client import UberRidesClient
from uber_rides.session import Session

YOUR_CLIENT_ID = 'izu_lOTQ_7qtqKJBBu3nHcYsUZGKNYCz'
YOUR_CLIENT_SECRET = 'hMmSHnXv0Y0lNM2aVHWbPIThR8aBqjAdbZ1oDHll'
YOUR_SERVER_TOKEN = 'UpT_gLFD7Qivj0X2kxsANocKLcipvr7Un_RCC1qe'
YOUR_REDIRECT_URL = 'http://localhost'
YOUR_PERMISSION_SCOPES = ['profile', 'history', 'places', 'request', 'request_receipt']
auth_flow = AuthorizationCodeGrant(
    YOUR_CLIENT_ID,
    YOUR_PERMISSION_SCOPES,
    YOUR_CLIENT_SECRET,
    YOUR_REDIRECT_URL,
)

# access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZXMiOltdLCJzdWIiOiJkYmQyM2I2NS00OTE1LTRkMTctODZlYi02MTdiZDc3YjMzMGUiLCJpc3MiOiJ1YmVyLXVzMSIsImp0aSI6IjYxYzczNDhmLTM2ZWEtNDVjNS1iMGVjLTExOWViMGI5ZWI0MiIsImV4cCI6MTQ5MjI5NDY0NiwiaWF0IjoxNDg5NzAyNjQ2LCJ1YWN0IjoiRk9CcGUwU0t6bURta1R4UWZud3VxMXN4b29oZkFJIiwibmJmIjoxNDg5NzAyNTU2LCJhdWQiOiJka1pVdWhXVFdWZnJMMXBFTzdpTTZGdWVrYTBJdGVORiJ9.laztOcN9BMCVszskRN6-i-cMjjrdsYcBJGrnyveA4YtIl3XPg8WAcNGCMqInAgMcx_tRJy4LPuVpWKdDp_cOI5dlYR0o4u9211CWSLL7QEN28mfvdw-J8-wcleaIgxOLlBJT5N0Dd0PVIo9uK84TvKhYQSPMST35RENGXyt-AnDvJaTeK4-VjP0bEJ7Lnm6WB1Ct9lX9panC5fUSlXcxy6X580CDYnj_QvK3p5jNxbYwJb4zlFGAre7DH4oiTnh17OHCO88vHn-j7AEsgt8mFtdDzYzC-K-dy5fpLU95Ec4cmN0Dlx_24RiO5Ip6ZEM4LgN_BH7ORP4IaeV6-0CEnw'



#Destination : 40.502744, -74.448545
auth_url = auth_flow.get_authorization_url()
print auth_url

st = auth_url.find('state=')

ns = auth_url[st+len('state='):]
state = ns[:ns.find('&')]

print state

# redirect_uri = YOUR_REDIRECT_URL + '?code=' + access_token  + '&state=' + state

# http://localhost/?state=o0tbQ7VtRzzBYtn0OALmjQY3XATB9UaU&code=fKW6qXnhmL1Naz6NvQ5TRwFkbZinNQ#_

redirect_uri = 'http://localhost/?state='+ state + '&code=DWeAJ380OvMFK87t0D2jIa96FogdUJ#_'
session = auth_flow.get_session(redirect_uri)
client = UberRidesClient(session)
credentials = session.oauth2credential

print credentials


# session = Session(server_token=YOUR_SERVER_TOKEN)
# client = UberRidesClient(session)
response = client.get_products(40.488101, -74.437934)
products = response.json.get('products')

product_id = products[0].get('product_id')
print products[0].get('display_name')
estimate = client.estimate_ride(
    product_id=product_id,
    start_latitude=40.488101,
    start_longitude=-74.437934,
    end_latitude=40.502744,
    end_longitude=-74.448545,
    seat_count=2
)

fare = estimate.json.get('fare')
print fare