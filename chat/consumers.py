import re
import json
import logging
from channels import Group
from channels.sessions import channel_session
from .models import Room


@channel_session
def ws_connect(message):

    # Could use more error handling here
    prefix, label = message['path'].strip('/').split('/')

    try:
        room = Room.objects.get(label=label)
        message.reply_channel.send({"accept": True})    # Accept connection
        print('Room : %s' % room.label)
    except Room.DoesNotExist:
        print('Room with label %s does not exist!' % label)
        return

    Group('chat-' + label).add(message.reply_channel)
    message.channel_session['room'] = room.label
    print(message.keys())

@channel_session
def ws_receive(message):
    # Could use more error handling here
    label = message.channel_session['room']

    try:
        room = Room.objects.get(label=label)
    except Room.ObjectDoesNotExist:
        print('Room with label %s does not exist!' % label)
        return

    # Get text message, and parse to json; throw any errors if any
    try:
        data = json.loads(message['text'])
    except ValueError:
        print('Oops! Your message isn\'t in json!')
        return

    # Make sure data is in proper format, i.e, { 'handle': ... , 'message': ... }
    if set(data.keys()) != {'handle', 'message'}:
        print('Improper message format : %s ', data)
        return

    msg = room.messages.create(handle=data['handle'], message=data['message'])
    response = json.dumps(msg.as_dict())

    Group('chat-' + label).send({'text': response})


@channel_session
def ws_disconnect(message):
    print('disconnecting')
    label = message.channel_session['room']
    Group('chat-' + label).discard(message.reply_channel)
