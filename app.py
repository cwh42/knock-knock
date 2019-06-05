from flask import Blueprint
from flask_restful import Api
from resources.Hello import Hello
from resources.Device import DeviceResource
from resources.Log import LogResource, LogsResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routeis
api.add_resource(Hello, '/Hello')
api.add_resource(DeviceResource, '/Device')
api.add_resource(LogResource, '/Log')
api.add_resource(LogsResource, '/Logs')
