from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
from .views import get_all_passwords
from .templatetags.password_filters import description,json_friendly
import json
from django.utils import timezone
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http  
# def http_consumer(message):
#     # Make standard HTTP response - access ASGI path attribute directly
#     response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
#     # Encode that response into message format (ASGI)
#     for chunk in AsgiHandler.encode_response(response):
#         message.reply_channel.send(chunk)

@http_session_user
def ws_connect(message):
	# check user's validity
	if not message.user.is_authenticated():
		message.reply_channel.send({'accept': False})
		return

	Group('users').add(message.reply_channel)
	# accept the connection
	message.reply_channel.send({'accept':True})

@http_session_user
def ws_message(message):
	content = message.content['text']
	if content.replace('\"','') == 'pw_list':
		pws = get_all_passwords()
		for pw in pws:
			pw = json_friendly(pw)
			# pw['date_created'] = str(timezone.now() - pw['date_created']).split(',')[0]
			# pw['description'] = description(pw['password'])
			message.reply_channel.send({
					'text': json.dumps(pw)
			})		
# @channel_session_user
@http_session_user
def ws_disconnect(message):
    Group('users').discard(message.reply_channel)
    message.user.is_active = False
    message.user.save()
    # close the user's session

