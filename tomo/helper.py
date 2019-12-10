from tomo.models import Event
from django.db.models import Q

def getEventWithTags(tags):
    ret = Event.objects
    if not tags:
        return ret.all()
    else:
        q = Q()
        for tag in tags:
            ret = ret.filter(tags__name__in=[tag])
        return ret.distinct()