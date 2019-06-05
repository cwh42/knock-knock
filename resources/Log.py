from flask import jsonify, request
from flask import current_app as app
from flask_restful import Resource
from Model import db, Log, Device, LogSchema, LogsSchema

many_logs_schema = LogSchema(many=True)
log_schema = LogSchema()
logs_schema = LogsSchema()

class LogResource(Resource):
    def get(self):
        logs = Log.query.all()
        logs = many_logs_schema.dump(logs).data
        return {"status":"success", "data":logs}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = log_schema.load(json_data)
        if errors:
            return {"status": "error", "data": errors}, 422
        
        log = Log.query.filter_by(mac=data['mac'], time=data['time']).first()
        if log:
            return {'message': 'Log entry already exists'}, 400
        
        mac = Device.query.filter_by(mac=data['mac']).first()
        if not mac:
            device = Device(
                mac=data['mac'],
                name=data['mac']
                )
            db.session.add(device)

        log = Log(
            mac=data['mac'],
            time=data['time']
            )
        db.session.add(log)
        db.session.commit()

        result = log_schema.dump(log).data

        return {'status': "success", 'data': result}, 201


class LogsResource(Resource):
    def get(self):
        logs = Log.query.all()
        logs = logs_schema.dump(logs).data
        return {"status":"success", "data":logs}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = logs_schema.load(json_data)
        if errors:
            return {"status": "error", "data": errors}, 422

        app.logger.info( "log: %s"% (str(data['logs'])) )

        result = ''
        
        for time, macs in data['logs'].items():
            for mac in macs:
                app.logger.info( "time: " + time + ", mac: " + mac )
                log = Log.query.filter_by(mac=mac, time=time).first()
                if log:
                    return {'message': 'Log entry already exists'}, 400
        
                mac_db = Device.query.filter_by(mac=mac).first()                
                if not mac_db:
                    device = Device(
                        mac=mac,
                        name=mac
                        )
                    db.session.add(device)

                log = Log(mac=mac, time=time)

                db.session.add(log)
                db.session.commit()
# fixme
                result = logs_schema.dump(log).data

        return {'status': "success", 'data': result}, 201
