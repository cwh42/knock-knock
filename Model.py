from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.types as types

# make use of netaddr

ma = Marshmallow()
db = SQLAlchemy()

class MacType(types.TypeDecorator):
    impl = types.BigInteger
    
    def process_bind_param(self, value, dialect):
        return (int(value.translate(str.maketrans('','',":.- ")), 16))
    
    def process_result_value(self, value, dialect):
        mac_hex = "{:012x}".format(value)
        return ":".join(mac_hex[i:i+2] for i in range(0, len(mac_hex), 2))

class Log(db.Model):
    __tablename__ = 'log'
    mac = db.Column(MacType, db.ForeignKey('devices.mac'), primary_key=True)
    time = db.Column(db.DateTime(timezone=True), primary_key=True)
    device_name = db.relationship('Device', backref='log')

    def __init__(self, time, mac):
        self.time = time
        self.mac = mac

class Device(db.Model):
    __tablename__ = 'devices'
    mac = db.Column(MacType, primary_key=True)
    name = db.Column(db.String(150))
    logs = db.relationship('Log', backref='device')

    def __init__(self, mac, name):
        self.mac = mac
        self.name = name

class DeviceSchema(ma.Schema):
    mac = fields.String(required=True)
    name = fields.String()

class LogSchema(ma.Schema):
    mac = fields.String(required=True)
    time = fields.DateTime(required=True)

class LogsSchema(ma.Schema):
    logs = fields.Dict(keys=fields.DateTime(require=True),
                       values=fields.List(fields.String()))
    
