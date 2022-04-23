from functools import wraps
from .token import decode
from flask import g,request, redirect, url_for, jsonify


def is_ajax():
    return request.headers.get('x-requested-with') == 'XMLHttpRequest' \
        or request.accept_mimetypes.best == 'application/json' \
        or (request.headers.has_key('Content-Type') and request.headers.get('Content-Type') == 'application/json')

def auth(next):

    @wraps(next)
    def check_auth(*args, **kwargs):
        ok, message = decode(request.headers.get('Authorization'))
        if ok:
            return next(*args, **kwargs)
        else:
            if is_ajax(): 
                return jsonify(message= message or "Not authorized."), 403
            else:
                return redirect(url_for('login', next=request.url))
        # if g.user is None:
        
    return check_auth