from database import db
from sqlalchemy import text

'''
TODOS:
    - [NOT DONE] How to tranform list of BSSIDs from database to this?
    - [NOT DONE] For every retrain, the MLS will fetch data from database. There is a potential
        of an AP will be deleted/updated/ new ones are added. Hence, the dictionary
        of AP has to follow the order of BSSIDs according to Acces sPint table (from DB).
        Solution:
        o Create new dictionary 'access_points' every time the db data is fetched. 
        o Check one-by-one list of APs from the database -> save the BSSID as the key, the order (index of BSSID) 
            as the value.
    - [NOT DONE] Use the dummy data variable using real ones -> duplicate the ones in GoogleCollab . Use ChatGPT for speed.
        o
'''

access_points = {}

''' 
    aps dict is a dictionary to store access points' BSSID. 
    The value of each key (BSSID) is the BSSID position on the original database table.
'''