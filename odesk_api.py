import odesk
import json
from pprint import pprint
import sys

def web_based_app():
    public_key = raw_input('Please enter public key: > ')
    secret_key = raw_input('Please enter secret key: > ')

    #Instantiating a client without an auth token
    client = odesk.Client(public_key, secret_key)

    print "Please go to this URL (authorize the app if necessary):"
    print client.auth.get_authorize_url()
    print "After that you should be redirected back to your app URL with " + \
          "additional ?oauth_verifier= parameter"

    verifier = raw_input('Enter oauth_verifier: ')
    
    oauth_access_token, oauth_access_token_secret = \
        client.auth.get_access_token(verifier)

    # Instantiating a new client, now with a token.
    # Not strictly necessary here (could just set `client.oauth_access_token`
    # and `client.oauth_access_token_secret`), but typical for web apps,
    # which wouldn't probably keep client instances between requests
    client = odesk.Client(public_key, secret_key,
                          oauth_access_token=oauth_access_token,
                          oauth_access_token_secret=oauth_access_token_secret)

    return client


if __name__ == '__main__':
    client = web_based_app()

    try:
	for skill in ['microsoft-excel','java','visual-basic','statistics','r','mysql','sql','data-science','medical-informatics','data-analysis']:
       	    for x in range(2000): #Rate limit is 5000 per day
	        fmat = {'skills':'{}'.format(skill)}
		# Scroll through all the pages
	        outp = client.provider_v2.search_providers(fmat,page_offset=x*100,page_size=100)
                print x, fmat, len(outp)
	        if len(outp) == 0:
	            break
                for xx in range(len(outp)):
	            with open('data/{}_{}_{}'.format(skill,x,xx),'w') as outfile:
		        json.dump(outp[xx],outfile)
    except Exception, e:
        print "Exception at %s %s" % (client.last_method, client.last_url)
        raise e
