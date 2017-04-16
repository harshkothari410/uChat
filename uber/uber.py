"""
	Uber Package for uChat
"""

from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.client import UberRidesClient
from uber_rides.session import Session
from uber import config

class Uber(object):
	"""
	Class for Uber package
	"""

	def __init__(self):
		"""
		Initialization function
		Generates Authorization URL when an object is created

		"""	

		# auth_flow :  OAuth 2.0 Authorization Code flow used to generate Authorization URL 
		self.auth_flow = AuthorizationCodeGrant(

			config.CLIENT_ID,
			config.PERMISSION_SCOPES,
			config.CLIENT_SECRET,
			config.REDIRECT_URL

			)

		# Authorization URL for user
		self.auth_url = self.auth_flow.get_authorization_url()

		# @fix me 
		# access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZXMiOltdLCJzdWIiOiJkYmQyM2I2NS00OTE1LTRkMTctODZlYi02MTdiZDc3YjMzMGUiLCJpc3MiOiJ1YmVyLXVzMSIsImp0aSI6IjYxYzczNDhmLTM2ZWEtNDVjNS1iMGVjLTExOWViMGI5ZWI0MiIsImV4cCI6MTQ5MjI5NDY0NiwiaWF0IjoxNDg5NzAyNjQ2LCJ1YWN0IjoiRk9CcGUwU0t6bURta1R4UWZud3VxMXN4b29oZkFJIiwibmJmIjoxNDg5NzAyNTU2LCJhdWQiOiJka1pVdWhXVFdWZnJMMXBFTzdpTTZGdWVrYTBJdGVORiJ9.laztOcN9BMCVszskRN6-i-cMjjrdsYcBJGrnyveA4YtIl3XPg8WAcNGCMqInAgMcx_tRJy4LPuVpWKdDp_cOI5dlYR0o4u9211CWSLL7QEN28mfvdw-J8-wcleaIgxOLlBJT5N0Dd0PVIo9uK84TvKhYQSPMST35RENGXyt-AnDvJaTeK4-VjP0bEJ7Lnm6WB1Ct9lX9panC5fUSlXcxy6X580CDYnj_QvK3p5jNxbYwJb4zlFGAre7DH4oiTnh17OHCO88vHn-j7AEsgt8mFtdDzYzC-K-dy5fpLU95Ec4cmN0Dlx_24RiO5Ip6ZEM4LgN_BH7ORP4IaeV6-0CEnw'

		# This section restores the state of the auth_url
		state = self.auth_url.find('state=')
		state_ns = self.auth_url[state+len('state='):]
		self.state = state_ns[:state_ns.find('&')]

	def get_login_url(self):
		"""
		Provides the authorization URL 
		
		@arguments
			None 

		@return
			authorization url
		"""
		return self.auth_url

	def get_products(self, redirect_uri, latitude, longitude):
		"""
		returns available uber products with authorization 
		
		@arguments
			redirect_uri : The the redirect url received after authorization 
			latitude : Latitude of requested location
			longitude : Longitude of requested location

		@return
			products : Return uber products for the given location
		"""

		# Creating Session
		session = self.auth_flow.get_session(redirect_uri)

		# creating client
		client = UberRidesClient(session)

		response = client.get_products(latitude, longitude)
		products = response.json.get('products')
		return products

	def get_estimate(self,redirect_uri,productId,source_longitude,source_latitude,dest_longitude,dest_latitude,count):
		"""
		Returns exact estimate for a ride 
		
		@arguments
			redirect_uri : The the redirect url received after authorization 
			productId : The product id for requested service
			source_latitude : Latitude of source location
			source_longitude : Longitude of source location
			dest_latitude : Latitude of destination 
			dest_longitude : Longitude of destination 
			count : Number of passengers

		@return
			estimate : The exact estimate for the request
		"""

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


	def available_products(self, latitude, longitude):
		"""
		returns available uber products without authorization using server token 
		
		@arguments
			latitude : Latitude of requested location
			longitude : Longitude of requested location

		@return
			products : Return uber products for the given location
		"""
		session = Session(server_token=config.SERVER_TOKEN)
		client = UberRidesClient(session)
		response = client.get_products(latitude, longitude)
		products = response.json.get('products')
		return products

	def rough_estimate(self, source_latitude, source_longitude, dest_latitude, dest_longitude, count):
		"""
		Returns rough estimate for a ride 
		
		@arguments
			source_latitude : Latitude of source location
			source_longitude : Longitude of source location
			dest_latitude : Latitude of destination 
			dest_longitude : Longitude of destination 
			count : Number of passengers

		@return
			estimate : The rough estimates for the request
		"""
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
			
	def get_history(self, redirect_uri):
		"""
		Returns previous user history

		@arguments 
			redirect_uri : The the redirect url received after authorization

		@return
			history : User Ride History
		"""
		session = self.auth_flow.get_session(redirect_uri)
		client = UberRidesClient(session)
		response = client.get_user_activity()
		history = response.json
		return history

	def get_user_profile(self, redirect_uri):
		"""
		Returns user profile 

		@arguments 
			redirect_uri : The the redirect url received after authorization

		@return
			profile : The users profile

		"""
		session = self.auth_flow.get_session(redirect_uri)
		client = UberRidesClient(session)
		response = client.get_user_profile()
		profile = response.json
		return profile






