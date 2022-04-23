import persistance, time, os
from web.api import Router
from web import api
from web.utils.auth import auth
from flask import Flask, render_template, request, Response, session, jsonify, abort
from flask_cors import CORS, cross_origin
from flask_peewee.rest import RestAPI, RestResource
# from persistance import models


from persistance.models import Detection, DetectionRequest, LostClaim, Plate


import uuid, os
import detector
import ocr
import hashlib, json
from .utils.config import env, load_dotenv

load_dotenv()

view_resorces = env('VIEW_PATH')

if not os.path.exists( os.path.dirname(__file__) + '/' + view_resorces ):
    print('I cannot find my body... Panicking...')
    exit()


persistance.utils.DB.Seed()

application = Flask(__name__, template_folder=view_resorces, static_url_path='/', static_folder='views/frontend/dist')

application.config.from_object(__name__)

# apis = RestAPI(application)

# apis.register(persistance.models.LostClaim)
# apis.setup()
# CORS(application)
cors = CORS(application, support_credentials=True)

application.config['CORS_HEADERS'] = 'Content-Type'

det = detector.Detector(
    weights='../config/yolov4_custom_4000.weights',
    config='../config/yolov4_custom.cfg',
    names='../config/model.names'
)

ocrEngine = ocr.OCR('../config/ServiceAccountToken.json')

router = Router(application)

router.enrollController(api.StolenController, '/api/lost/')
router.enrollController(api.DetectionContoller, '/api/detections/')


@application.route('/login')
def login():
    return "No done yet!"

@application.route('/')
# @auth
def hello():
    data={   }
    return render_template( "index.html", data={})


@application.route('/preview/<key>')
def test(key):
    file = f'./{key}'.replace('---', '/')
    if os.path.exists(file):
        with open(file, 'rb') as f:
            return Response( f.read(), mimetype='image/jpg')
    
    abort(404)
    
@application.route('/detect', methods=['POST'])
# @auth
def detect():
    # print(request.files['image'].read())

    startTick = time.perf_counter()

    ip = str(request.remote_addr)

    imageBlob = request.files['image'].read()

    images = det.detect(imageBlob)

    

    session_id = hashlib.md5(imageBlob).hexdigest()

    dir = f'temp/{session_id}'
    
    files = dict()

    if not os.path.exists(dir):
        os.makedirs(dir)
        detectionRequest = DetectionRequest(image=f'{dir}/detection.jpg', user_id=1, ip=ip)
        detectionRequest.save()
        files['time'] = time.perf_counter() - startTick

        for key in images:
            file = f'{dir}/{key}.jpg'
            number = 'NA'
            if key != 'detection':
                number = ocrEngine.Process(images[key])
            files[key] = {
                'plate': file.replace('/', '---'),
                'number': number,
                'lost': LostClaim.select().join(Plate).where((Plate.number == number) & ( LostClaim.state == 1 ) ).count() > 0
            }
            det.writeToFile(f'./{file}', images[key])
            if number != 'NA' :
                plate, ok = Plate.get_or_create(number=number, remarks='')
                Detection(request_id=detectionRequest, plate_id=plate.id, ip=ip).save()

        with open(f'{dir}/data.json', 'w') as fp:
            json.dump(files, fp)
    else:
        with open(f'{dir}/data.json', 'r') as fp:
            files = json.load(fp)
            for file in files:
                # print('##### HERE #####', files[file]['number'])
                files[file]['lost'] = LostClaim.select().join(Plate).where((Plate.number == files[file]['number']) & ( LostClaim.state == 1 ) ).count() > 0

        
        # session[ref] = 
    # det.detect()
    return  jsonify(
        files= files
    )