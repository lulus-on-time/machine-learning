from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

# Entities
# class AccessPoint(db.Model):
#     __tablename__ = 'AccessPoint'
#     id = db.Column(db.Integer, primary_key=True)
#     bssid = db.Column(db.String(), unique=True)
#     ssid = db.Column(db.String())
#     description = db.Column(db.String())
#     # fingerprints ?? listofFngerprintDetail
#     # coordinate Coordinate ?? add another class "Coordinate"? 
#     # coordinateId ?? same as above

#     def __repr__(self):
#         return f"<Car {self.bssid}>"

# class Fingerprint(db.Model):
#     __tablename__ = 'Fingerprint'
#     id = db.Column(db.Integer, primary_key=True)
#     createdAt = db.Column(db.DateTime, default=now())
#     # fingerprintDetails ?? listofFngerprintDetail
#     location = db.Column(db.String)

# class FingerprintDetail(db.Model):
#     __tablename__ = 'FingerprintDetail'
#     id = db.Column(db.Integer, primary_key=True)
#     # fp FP ?? add relation to another class FP, how syntax? 
#     fingerprintId = db.Column(db.Integer, unique=True)
#     # ap AcessPoint ?? add relation to another class AP, how syntax? 
#     bssid = db.Column(db.String)
#     rssi = db.Column(db.Float)
