from django.shortcuts import render
import requests
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import redirect
from django.conf import settings
from django.core.cache import cache
import logging
import urllib
logger = logging.getLogger(__name__)

class OAuth2CallbackView(View):
    """
    A Django view to handle the OAuth2 callback and exchange the authorization code
    for an access token.
    """

    def get(self, request):
        # Extract the authorization code from the callback request
        authorization_code = request.GET.get('code')
        if not authorization_code:
            return JsonResponse({'error': 'Authorization code not provided'}, status=400)

        # Define the token endpoint and payload
        token_endpoint = settings.OAUTH2_PROVIDER_TOKEN_URL
        client_id = settings.OAUTH2_CLIENT_ID
        client_secret = settings.OAUTH2_CLIENT_SECRET
        redirect_uri = settings.OAUTH2_REDIRECT_URI

        payload = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        }

        # Make a POST request to exchange the authorization code for an access token
        try:
            response = requests.post(token_endpoint, data=payload)
            response_data = response.json()

            if response.status_code == 200:
                cache.set('ACCESS_TOKEN', response_data['access_token'], timeout=3900)
                cache.set('REFRESH_TOKEN', response_data['refresh_token'], timeout=3900)
                # return JsonResponse(response_data)
                logger.info(response_data)
                return redirect('/')
            else:
                return JsonResponse({'error': response_data}, status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({'error': 'An error occurred while requesting the access token', 'details': str(e)}, status=500)


class OAuth2LoginView(View):
    """
    A Django view to redirect users to the OAuth2 provider's authorization page.
    """

    def get(self, request):
        logger.info('OAuth2LoginView')
        authorization_url = settings.OAUTH2_PROVIDER_AUTHORIZATION_URL
        client_id = settings.OAUTH2_CLIENT_ID
        redirect_uri = settings.OAUTH2_REDIRECT_URI
        scope = settings.OAUTH2_SCOPE
        encoded_scope = urllib.parse.quote(scope)
        # Build the authorization URL
        auth_url = (
            f"{authorization_url}?response_type=code&client_id={client_id}"
            f"&redirect_uri={redirect_uri}&scope={encoded_scope}")
        try:
            if cache.get('ACCESS_TOKEN'):
                return HttpResponse('You are already logged in')
            else:
                return redirect(auth_url)
        except KeyError:
            return redirect('login')


        
