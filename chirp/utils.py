
import traceback
from django.utils import simplejson
from django.http import HttpResponse
from chirp import log

def as_json(handler):
    def makejson(*args, **kwargs):
        try:
            r = handler(*args, **kwargs)
            status = 200
        except Exception, err:
            log.exception("in JSON response")
            r = {
                'success':False,
                'error': repr(err),
                'traceback': traceback.format_exc()
            }
            status = 500
        return HttpResponse(simplejson.dumps(r), 
                            mimetype='application/json', 
                            status=status )
    return makejson