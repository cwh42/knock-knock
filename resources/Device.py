from flask import request
from flask_restful import Resource
from Model import db, Device, DeviceSchema

devices_schema = DeviceSchema(many=True)
device_schema = DeviceSchema()

class DeviceResource(Resource):
    def get(self):
        devices = Device.query.all()
        devices = devices_schema.dump(devices).data
        return {'status': 'success', 'data': devices}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = device_schema.load(json_data)
        if errors:
            return errors, 422
        device = Device.query.filter_by(mac=data['mac']).first()
        if device:
            return {'message': 'Device already exists'}, 400
        device = Device(
            mac=data['mac'],
            name=data['name'] or data['mac']
            )

        db.session.add(device)
        db.session.commit()

        result = device_schema.dump(device).data

        return { "status": 'success', 'data': result }, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = device_schema.load(json_data)
        if errors:
            return errors, 422
        device = Device.query.filter_by(mac=data['mac']).first()
        if not device:
            return {'message': 'Device does not exist'}, 400
        device.name = data['name']
        db.session.commit()

        result = device_schema.dump(device).data

        return { "status": 'success', 'data': result }, 204

#    def delete(self):
#        json_data = request.get_json(force=True)
#        if not json_data:
#               return {'message': 'No input data provided'}, 400
#        # Validate and deserialize input
#        data, errors = device_schema.load(json_data)
#        if errors:
#            return errors, 422
#        device = Device.query.filter_by(mac=data['mac']).delete()
#        db.session.commit()
#
#        result = device_schema.dump(device).data
#
#        return { "status": 'success', 'data': result}, 204
