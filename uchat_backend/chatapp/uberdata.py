from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.client import UberRidesClient
from uber_rides.session import Session
from geopy.geocoders import Nominatim
geolocator = Nominatim()


YOUR_CLIENT_ID = 'dkZUuhWTWVfrL1pEO7iM6Fueka0IteNF'
YOUR_CLIENT_SECRET = '7ZMw7r_gvf70djT86qebOSfTofB_zNnwyRwnoE_l'
YOUR_SERVER_TOKEN = '7jj733zk0UYqhcN5UjXsZFF9WPJ7Fkin6zSik9ZB'
YOUR_REDIRECT_URL = 'http://localhost'
YOUR_PERMISSION_SCOPES = ['profile', 'history', 'places', 'request', 'request_receipt']
auth_flow = AuthorizationCodeGrant(
    YOUR_CLIENT_ID,
    YOUR_PERMISSION_SCOPES,
    YOUR_CLIENT_SECRET,
    YOUR_REDIRECT_URL,
)

auth_url = auth_flow.get_authorization_url()

st = auth_url.find('state=')

ns = auth_url[st+len('state='):]
state = ns[:ns.find('&')]
print auth_url
print state





def json_string(data):

	ans = ''
	# u'display_name, u'estimate, u'distance
	for l in data:
		name = l.get('display_name')
		price = l.get('estimate')
		distance = l.get('distance')

		temp = str(name) + ': ' + str(distance) + ' miles ' + str(price) + '\n'

		ans += temp

	return ans



def get_uber_data(location):
	log_lat = geolocator.geocode(location)

	print log_lat.latitude, log_lat.longitude
	print "OK"
	# response = client.get_products(log_lat.latitude, log_lat.longitude)
	# session = self.auth_flow.get_session(redirect_uri)
	session = Session(server_token=YOUR_SERVER_TOKEN)
	client = UberRidesClient(session)

	# print client

	start = geolocator.geocode('Hill Center, Piscataway')
	print start.latitude, start.longitude
	# response = client.get_products(log_lat.latitude, log_lat.longitude)
	
	print client
	response = client.get_price_estimates(
		start_latitude=start.latitude,
		start_longitude=start.longitude,
		end_latitude=log_lat.latitude,
		end_longitude=log_lat.longitude,
		seat_count=2
	)

	print response
	ans = json_string(response.json.get('prices'))


	print ans

	return ans
