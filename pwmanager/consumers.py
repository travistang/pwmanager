from django.http import HttpResponse
from channels.handler import AsgiHandler,AsgiRequest
from channels import Group
from .views import get_all_passwords
from .models import AuthorizedToken
from .templatetags.password_filters import description,json_friendly
import json
from urllib.parse import urlparse,parse_qs
from django.utils import timezone
from channels.auth import http_session_user, channel_session_user_from_http,channel_session  
from django.contrib.sessions.models import Session
from django.contrib.auth import SESSION_KEY
from datetime import timedelta

def validate_socket_message(message):
	if type(message) != dict: # should have parsed it beforehand
		return False
	return not ('action' not in message or ('session_key' not in message and 'token' not in message))

# an authenticated user should have either a session_key or token
# validate_socket_message is expected to be called before this function or error will occur
def is_socket_user_authenticated(message):
	if 'session_key' in message: # session_key is given
		key = message['session_key']
		try:
			session = AuthorizedToken.objects.get(token=key)
			return True
		except Exception as e:
			print(e)
			# the key is not valid
			return False
	else: # token is given
		key = message['token']
		return AuthorizedToken.objects.filter(token = key).exists()

@http_session_user
# @channel_session_user_from_http
def ws_connect(message):
	# check user's validity
	print('receive connection request from ',message.user)

	if not message.user.is_authenticated():
		print('rejecting request from',message.user)
		message.reply_channel.send({'accept': False})
		return

	Group('users').add(message.reply_channel)

	# handle browser request
	# create a 30-minute token for browser users
	token = AuthorizedToken.create_and_get_token(expiry_date = timezone.now() + timedelta(minutes = 30))
	# accept the connection

	message.reply_channel.send({'accept':True})
	message.reply_channel.send({'text':json.dumps({'token':token})})

@http_session_user
def ws_message(message):
	print('received a message',message.content['text'])
	content = message.content['text']
	content = json.loads(content)

	# verify key
	if not validate_socket_message(content) or not is_socket_user_authenticated(content):
		return

	if content['action'] == 'pw_list':
		pws = get_all_passwords()
		for pw in pws:
			pw = json_friendly(pw)
			message.reply_channel.send({
					'text': json.dumps(pw)
			})
		# add a message to indicate that there are no more passwords to send
		message.reply_channel.send({
					'text': json.dumps({"action": "done"})
			})

@http_session_user
def ws_disconnect(message):
	print('receive message from ',message.user)
	Group('users').discard(message.reply_channel)
# close the user's session

