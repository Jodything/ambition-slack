from django.db import models, IntegrityError

from ambition_slack.slack.models import SlackUser


class PagerdutyUser(models.Model):
    slack_user = models.OneToOneField(SlackUser)
    email = models.TextField(unique=True)

    def __unicode__(self):
        return self.email


class PagerdutyEventReceiptManager(models.Manager):
    def create_event_receipt(self, incident_id, incident_type):
        try:
            return PagerdutyEventReceipt.objects.create(incident_id=incident_id, incident_type=incident_type)
        except IntegrityError:
            return None


class PagerdutyEventReceipt(models.Model):
    RESOLVE = 'incident.resolve'
    TRIGGER = 'incident.trigger'
    #
    incident_id = models.CharField(max_length=64)

    #
    incident_type = models.CharField(max_length=64, choices=(
        (RESOLVE, 'resolve'),
        (TRIGGER, 'trigger')
    ))

    objects = PagerdutyEventReceiptManager()

    class Meta:
        unique_together = ('incident_id', 'incident_type')
