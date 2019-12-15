from tomo.models import Event, User
from django.db.models import Q

def getEventWithTags(tags):
    ret = Event.objects
    if not tags:
        # if there is no tag
        return ret.all()
    else:
        q = Q()
        for tag in tags:
            # chain filteration
            ret = ret.filter(tags__name__in=[tag])
        return ret.distinct()

def getCurrentUserId(request):
    return request.session['user_id']

# receive request object, user id
def setUserId(request, user_id=0, username=""):
    if user_id != 0:
        request.session['user_id'] = user_id
    elif username:
        request.session['user_id'] = User.objects.get(username=username).id
    else:
        raise ValueError("Invalid argument: user_id={}\nusername={}".format(user_id, username))

def deleteCookieUserId(request):
    try:
        del request.session['user_id']
    except:
        pass