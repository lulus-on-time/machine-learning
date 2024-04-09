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

'''

access_points = {
    '38:17:C3:18:00:60': 0,
    '38:17:C3:18:00:63': 1,
    '38:17:C3:18:00:83': 2,
    '38:17:C3:18:01:60': 3,
    '38:17:C3:18:05:E0': 4,
    '38:17:C3:18:06:60': 5,
    '38:17:C3:18:06:63': 6,
    '38:17:C3:18:0C:E0': 7,
    '38:17:C3:18:0C:E1': 8,
    '38:17:C3:18:14:20': 9,
    '38:17:C3:1A:05:20': 10,
    '38:17:C3:1A:05:21': 11,
    '38:17:C3:1A:0A:21': 12,
    '38:17:C3:2A:0C:80': 13,
    '38:17:C3:2A:0C:81': 14,
    '38:17:C3:2A:0E:00': 15,
    '38:17:C3:2A:0E:01': 16,
    '38:17:C3:2A:10:A1': 17,
    '38:17:C3:2A:11:60': 18,
    '38:17:C3:2A:11:61': 19,
    '38:17:C3:2A:12:E0': 20,
    '38:17:C3:2A:12:E3': 21,
    '38:17:C3:2A:16:C0': 22,
    '38:17:C3:2A:16:C1': 23,
    '38:17:C3:2A:16:E0': 24,
    '38:17:C3:2A:16:E1': 25,
    '38:17:C3:2A:1A:80': 26,
    '38:17:C3:2A:1A:81': 27,
    '38:17:C3:2A:1F:00': 28,
    '38:17:C3:2A:25:80': 29,
    '38:17:C3:2A:25:81': 30,
    '38:17:C3:2A:30:00': 31,
    '38:17:C3:2A:30:01': 32,
    '38:17:C3:2A:31:C1': 33,
    '38:17:C3:2A:32:20': 34,
    '38:17:C3:2A:3D:C0': 35,
    '38:17:C3:2A:3D:C1': 36,
    '38:17:C3:2A:40:80': 37,
    '38:17:C3:2A:40:83': 38,
    '38:17:C3:2A:40:C0': 39,
    '38:17:C3:2A:40:C3': 40,
    '38:17:C3:2A:41:E0': 41,
    '38:17:C3:2A:41:E1': 42,
    '38:17:C3:2A:43:20': 43,
    '38:17:C3:2A:49:80': 44,
    '38:17:C3:2A:49:C0': 45,
    '38:17:C3:2A:4A:80': 46,
    '9C:1C:12:D7:F4:A0': 47,
    '9C:1C:12:D7:F4:A1': 48,
    '9C:1C:12:D7:FE:E0': 49,
    '9C:1C:12:D7:FE:E1': 50
}

''' 
    aps dict is a dictionary to store access points' BSSID. 
    The value of each key (BSSID) is the BSSID position on the original database table.
'''