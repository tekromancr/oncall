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
  from django.db.transaction import atomic
  @atomic
  def process_message(message):
    data = json.loads(message.content['text'])
    def update_light(data):
      if "position" not in data:
        light = Light.objects.get(pk=data['pk'])
      else:
        light = Light.objects.get(position=data['position'])

      light.color = data['color']
      light.save()

    try: # if we only got a single datapoint
        update_light(data)
    except Exception:
      for light_data in data:
        update_light(light_data)
    Group('lights').send(
        {'text': json.dumps(
            {'lights': list(
                Light.objects.all().values('pk','color','position','assigned_user__username')
            )}
        )}
    )
  process_message(message)

@channel_session
def ws_disconnect(message):
    Group('light').discard(message.reply_channel)
