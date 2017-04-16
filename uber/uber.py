
import config
from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.client import UberRidesClient
from uber_rides.session import Session

# uber pool
UFP_PRODUCT_ID = '26546650-e557-4a7b-86e7-6a3942445247'

# uber black
SURGE_PRODUCT_ID = 'd4abaae7-f4d6-4152-91cc-77523e8165a4'

class Uber:
	state=''
	# auth_flow=''

	def __init__(self):
		
		self.auth_flow=AuthorizationCodeGrant(

			config.CLIENT_ID,
			config.PERMISSION_SCOPES,
			config.CLIENT_SECRET,
			config.REDIRECT_URL

			)
		self.auth_url=self.auth_flow.get_authorization_url()
		# FIX ME
		# access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZXMiOltdLCJzdWIiOiJkYmQyM2I2NS00OTE1LTRkMTctODZlYi02MTdiZDc3YjMzMGUiLCJpc3MiOiJ1YmVyLXVzMSIsImp0aSI6IjYxYzczNDhmLTM2ZWEtNDVjNS1iMGVjLTExOWViMGI5ZWI0MiIsImV4cCI6MTQ5MjI5NDY0NiwiaWF0IjoxNDg5NzAyNjQ2LCJ1YWN0IjoiRk9CcGUwU0t6bURta1R4UWZud3VxMXN4b29oZkFJIiwibmJmIjoxNDg5NzAyNTU2LCJhdWQiOiJka1pVdWhXVFdWZnJMMXBFTzdpTTZGdWVrYTBJdGVORiJ9.laztOcN9BMCVszskRN6-i-cMjjrdsYcBJGrnyveA4YtIl3XPg8WAcNGCMqInAgMcx_tRJy4LPuVpWKdDp_cOI5dlYR0o4u9211CWSLL7QEN28mfvdw-J8-wcleaIgxOLlBJT5N0Dd0PVIo9uK84TvKhYQSPMST35RENGXyt-AnDvJaTeK4-VjP0bEJ7Lnm6WB1Ct9lX9panC5fUSlXcxy6X580CDYnj_QvK3p5jNxbYwJb4zlFGAre7DH4oiTnh17OHCO88vHn-j7AEsgt8mFtdDzYzC-K-dy5fpLU95Ec4cmN0Dlx_24RiO5Ip6ZEM4LgN_BH7ORP4IaeV6-0CEnw'

		# Authorization URL
		st = self.auth_url.find('state=')
		ns = self.auth_url[st+len('state='):]
		self.state = ns[:ns.find('&')]

	def get_login_url(self):
		return self.auth_url

	def get_products(self,redirect_uri,latitude,longitude):
		# Creating Session
		session = self.auth_flow.get_session(redirect_uri)

		# creating client
		client = UberRidesClient(session)

		response = client.get_products(latitude,longitude)
		products = response.json.get('products')
		return products

	def get_estimate(self,redirect_uri,productId,source_longitude,source_latitude,dest_longitude,dest_latitude,count):
		session = self.auth_flow.get_session(redirect_uri)
		client = UberRidesClient(session)
		response = client.estimate_ride(
			product_id=productId,
			start_latitude=source_latitude,
			start_longitude=source_longitude,
			end_latitude=dest_latitude,
			end_longitude=dest_longitude,
			seat_count=count
		)

		estimate = response.json.get('prices')
		return estimate


	def available_products(self,latitude,longitude):
		session = Session(server_token=config.SERVER_TOKEN)
		client = UberRidesClient(session)
		response = client.get_products(latitude,longitude)
		products = response.json.get('products')
		return products

	def average_estimate(self,source_latitude,source_longitude,dest_latitude,dest_longitude,count):

		session = Session(server_token=config.SERVER_TOKEN)
		client = UberRidesClient(session)
		response = client.get_price_estimates(
			start_latitude=source_latitude,
			start_longitude=source_longitude,
			end_latitude=dest_latitude,
			end_longitude=dest_longitude,
			seat_count=count
		)

		estimate = response.json.get('prices')
		return estimate
			
	def get_history(self,redirect_uri):
		session = self.auth_flow.get_session(redirect_uri)
		client = UberRidesClient(session)
		response = client.get_user_activity()
		history = response.json
		return history

	def get_user_profile(self,redirect_uri):
		session = self.auth_flow.get_session(redirect_uri)
		client = UberRidesClient(session)
		response = client.get_user_profile()
		profile = response.json
		return profile





