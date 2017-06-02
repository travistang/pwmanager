from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group

def http_consumer(message):
    # Make standard HTTP response - access ASGI path attribute directly
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    # Encode that response into message format (ASGI)
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)

def ws_message(message):
	# ASGI WebSocket packet-received and send-packet message types
	# both have a "text" key for their textual data.
	message.reply_channel.send({
	    "text": message.content['text'],
	})

def ws_connect(message):
	Group('users').add(message.reply_channel)

def ws_disconnect(message):
    Group('users').discard(message.reply_channel)
