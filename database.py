from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

# from app import db
# print("Hello")
# for table_name in app.db.Model.metadata.tables:
#     print(table_name)
#     print("Hello")

# with app.app_context():
#     db.reflect()

# class Base(DeclarativeBase):
#   pass

# db = SQLAlchemy(model_class=Base)
# db.init_app(app)

# with app.app_context():
#     db.reflect()

# class AccessPoint(db.Model):
#     __table__ = db.Model.metadata.tables['AccessPoint']

#     def __repr__(self):
#         return self.id

# class Coordinate(db.Model):
#     __table__ = db.Model.metadata.tables['Coordinate']

#     def __repr__(self):
#         return self.id
    
# class Fingerprint(db.Model):
#     __table__ = db.Model.metadata.tables['Fingerprint']

#     def __repr__(self):
#         return self.id
    
# class FingerprintDetail(db.Model):
#     __table__ = db.Model.metadata.tables['FingerprintDetail']

#     def __repr__(self):
#         return self.id

# class Floor(db.Model):
#     __table__ = db.Model.metadata.tables['Floor']

#     def __repr__(self):
#         return self.id

# class Room(db.Model):
#     __table__ = db.Model.metadata.tables['Room']

#     def __repr__(self):
#         return self.id

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
