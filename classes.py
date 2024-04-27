from database import db

def execute():
    class AccessPoint(db.Model):
        __table__ = db.Model.metadata.tables['AccessPoint']

        def __repr__(self):
            return self.id
        
    class Coordinate(db.Model):
        __table__ = db.Model.metadata.tables['Coordinate']

        def __repr__(self):
            return self.id
            
    class Fingerprint(db.Model):
        __table__ = db.Model.metadata.tables['Fingerprint']

        def __repr__(self):
            return self.id
            
    class FingerprintDetail(db.Model):
        __table__ = db.Model.metadata.tables['FingerprintDetail']

        def __repr__(self):
            return self.id

    class Floor(db.Model):
        __table__ = db.Model.metadata.tables['Floor']

        def __repr__(self):
            return self.id

    class Room(db.Model):
        __table__ = db.Model.metadata.tables['Room']

        def __repr__(self):
            return self.id
    
    class Network(db.Model):
        __table__ = db.Model.metadata.tables['Network']

        def __repr__(self):
            return self.id
        
    class Schedule(db.Model):
        __table__ = db.Model.metadata.tables['Schedule']

        def __repr__(self):
            return self.id
        
    class Subject(db.Model):
        __table__ = db.Model.metadata.tables['Subject']

        def __repr__(self):
            return self.id
                
    class User(db.Model):
        __table__ = db.Model.metadata.tables['User']

        def __repr__(self):
            return self.id
    
    return {
        "AccessPoint": AccessPoint,
        "Coordinate": Coordinate,
        "Fingerprint": Fingerprint,
        "FingerprintDetail": FingerprintDetail,
        "Floor": Floor,
        "Room":Room,
        "Network":Network,
        "Schedule":Schedule,
        "Subject":Subject,
        "User":User
    }
