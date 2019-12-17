from tomo.models import Event, User
from django.db.models import Q

NO_USER = 0

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
    # if there is session
    if 'user_id' in request.session and request.session['user_id']:
        user_id = request.session['user_id']
        try:
            user = User.objects.get(pk=user_id)
        except:
            return NO_USER
        return request.session['user_id']
    else:
        # default 0 is no user
        return NO_USER

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