from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
from .views import get_all_passwords
from .templatetags.password_filters import description,json_friendly
import json
from django.utils import timezone

def http_consumer(message):
    # Make standard HTTP response - access ASGI path attribute directly
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    # Encode that response into message format (ASGI)
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)
def ws_connect(message):
	Group('users').add(message.reply_channel)
	
	# accept the connection
	message.reply_channel.send({'accept':True})

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
	# message.reply_channel.send({
	#     "text": message.content['text'],
	# })





def ws_disconnect(message):
    Group('users').discard(message.reply_channel)
