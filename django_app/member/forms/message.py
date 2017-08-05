from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django_messages.forms import ComposeForm
from django_messages.models import Message
if "pinax.notifications" in settings.INSTALLED_APPS and getattr(settings, 'DJANGO_MESSAGES_NOTIFY', True):
    from pinax.notifications import models as notification
else:
    notification = None


User = get_user_model()

class NewComposeForm(ComposeForm):
    recipient = forms.ModelChoiceField(label='받아랏!', queryset=User.objects.all())

    def save(self, sender, parent_msg=None):
        recipients = self.cleaned_data['recipient']
        subject = self.cleaned_data['subject']
        body = self.cleaned_data['body']
        message_list = []
        msg = Message(
            sender=sender,
            recipient=recipients,
            subject=subject,
            body=body,
        )
        if parent_msg is not None:
            msg.parent_msg = parent_msg
            parent_msg.replied_at = timezone.now()
            parent_msg.save()
        msg.save()
        message_list.append(msg)
        if notification:
            if parent_msg is not None:
                notification.send([sender], "messages_replied", {'message': msg,})
                notification.send([r], "messages_reply_received", {'message': msg,})
            else:
                notification.send([sender], "messages_sent", {'message': msg,})
                notification.send([r], "messages_received", {'message': msg,})
        return message_list
