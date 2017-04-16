from uber import Uber
from pprint import pprint

test_client = Uber()
auth_url = test_client.get_login_url()
print auth_url
# print test_client.state

redirect_uri = 'http://localhost/?state='+ test_client.state + '&code=iaBtf8KQgZnCvgHjFP6mFQ468yHZU4#_'


# Testing Products
# products=test_client.get_products(redirect_uri,40.488284559450236, -74.4375792145729)


# Testing Available Products
# products=test_client.available_products(40.488284559450236, -74.4375792145729)
# pprint(products)


# Testing Average Estimates
# estimate=test_client.average_estimate(40.488284559450236,-74.4375792145729,40.51743689664695,-74.45940971374512,2)
# pprint(estimate)

# Actual Estimate
# estimate=test_client.get_estimate(redirect_uri,product_id,40.488284559450236,-74.4375792145729,40.51743689664695,-74.45940971374512,2)
# pprint(estimate)


# Testing user history
# history=test_client.get_history(redirect_uri)
# pprint(history)

# Testing User Profile
# profile=test_client.get_user_profile(redirect_uri)
# pprint(profile)