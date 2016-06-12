import json

from channels import Group
from channels.sessions import channel_session
from lights.models import Light

@channel_session
def ws_connect(message):
    Group('lights').add(message.reply_channel)
    Group('lights').send(
        {'text': json.dumps(
            {'lights':list(
                Light.objects.all().values('pk','color','position','assigned_user__username')
            )}
        )}
    )

@channel_session
def ws_receive(message):
    data = json.loads(message.content['text'])
    light = Light.objects.get(pk=data['pk'])
    color = data['color']
    light.color = color
    light.save()
    Group('lights').send(
        {'text': json.dumps(
            {'lights': list(
                Light.objects.all().values('pk','color','position','assigned_user__username')
            )}
        )}
    )

@channel_session
def ws_disconnect(message):
    Group('light').discard(message.reply_channel)