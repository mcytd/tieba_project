import json, os
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

class SimpleUser:
    def __init__(self, username, permission_level):
        self.username = username
        self.permission_level = permission_level
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def __str__(self):
        return self.username

class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        username = request.session.get('username')
        if username:
            path = os.path.join(settings.BASE_DIR, 'userlist.json')
            try:
                with open(path, 'r') as f:
                    users = json.load(f)
                for u in users:
                    if u['username'] == username:
                        request.user = SimpleUser(username, u.get('permission_level', 4))
                        break
                else:
                    request.user = AnonymousUser()
            except:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()
        return self.get_response(request)
