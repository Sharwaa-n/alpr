
import json
from os import error
from flask.globals import request
from flask.views import MethodView
from flask.json import jsonify
import web
from persistance.models import Detection, Plate, LostClaim
from math import ceil

API_PREFIX='api'

class Router:

    application = None
    routes = dict()


    def __init__(self, app) -> None:
        self.application = app 

    def enrollController(self, controller, prefix=''):
        self.application.add_url_rule(prefix, view_func=controller.as_view(f'{prefix}-get-post'))
        self.application.add_url_rule(f'{prefix}/<int:id>', view_func=controller.as_view(f'{prefix}-get-patch-put'),methods=['PATCH', 'PUT'])
        # if isRest:
        #     if self.hasResource(controller, 'index'):
        #         self.register_route(f'/{controller}', controller.index)
        #     if self.hasResource(controller, 'get'):
        #         self.register_route(f'/{controller}/<id>', controller.get)
        #     if self.hasResource(controller, 'create'):
        #         self.register_route(f'/{controller}/<id>', controller.create)

        
    def hasResource(self, object, method):
        return hasattr(object, method) and callable(getattr(object, method, None))

    def register_route(self, route, func):
        if not route in self.routes:
            print('Route being regd:', route)
            
            self.application.add_url_rule(f'/{API_PREFIX}/{route}', view_func=func)
            self.routes[route] = func


    

class BaseController(Router, MethodView):
    
    def __str__(self):
        return str(self.__class__.__name__)[:-10].lower()


class DetectionContoller(BaseController):

    def __init__(self):
        # self.route('/<id>', self.get)
        pass

    def get(self):
        data = [ x.serialize for x in  Detection().select().paginate(1, 10)]
        return jsonify(data=data)


    
    def post(self):
        detection = Detection()
        if detection.Validate():
            return "Wow"
        else:
            return jsonify(errors=detection.errors), 406

class StolenController(BaseController):

    def __init__(self):
        # self.route('/<id>', self.get)
        pass
    
    def get(self):
        # return jsonify(data=[ x for i in Detection.select().paginate(page=1)])
        # page = 1 if request.query_string.has('page') request.query_string['page']
        page = 1
        if 'page' in request.args.keys(): 
            page = int(request.args.get('page'))

        query = LostClaim.select()

        if 'q' in request.args.keys() and len(request.args['q']) > 0:
            print("adding where clause...")
            query = query.join(Plate).where(Plate.number.contains(request.args['q']))
        # request.query_string['page'] or 1
        pageSize=12
        total_items = query.count()
        total_pages = ceil(total_items/pageSize)
        # print(range(page, total_pages), page, total_pages)
        print(query.sql())
        # min = page if page < 1 else (  )
        return jsonify(
            data=[i.serialize for i in query.order_by(-LostClaim.id).paginate(page, pageSize)],
            # data=list(.dicts() ),
            pager= {
                "page": page,
                # "has_next": page < total_pages,
                # "pages": [1, [x for x in range(page, total_pages+1)] , total_pages],
                # "has_previous": page > 1,
                "total_pages": total_pages,
                "total_items": total_items,
            }
        )


    def put(self, id):
        claim = LostClaim().select().where(LostClaim.id == id).get()
        claim.state = request.json['state']
        claim.save()
        return jsonify(claim.serialize)

    def post(self):


        claim = LostClaim(request.json)
       
        if 'plate' in request.json:
            plate = Plate.get_or_none( (Plate.number==request.json['plate'] ) )
            if plate is None:
                plate = Plate(number=request.json['plate'], remarks=request.json['remarks'])
                plate.save()

            claim.plate = plate
            
        claim.remarks = request.json['remarks']
        claim.user = 1
        if claim.Validate():
            claim.save()
            return jsonify(claim.serialize), 201
        else:
            return jsonify(errors=claim.errors), 406
