from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

import time
import os



def GetAbsScriptPath():
    AbsScriptPath = os.path.abspath( __file__ )
    AbsScriptPath_no_extension = AbsScriptPath.rpartition('.')[0]
    if not AbsScriptPath_no_extension:
        AbsScriptPath_no_extension = AbsScriptPath
    return (AbsScriptPath, AbsScriptPath_no_extension)
    
def get_db():
    strDatabasePath = GetAbsScriptPath()[1] + '.json'
    # using read and write cache to reduce i/o. later must use With to close db and commit changes
    db = TinyDB(strDatabasePath, storage=CachingMiddleware(JSONStorage))
    return db
        
        
def get_ts():
    with get_db() as db:
        q = Query()
        lst_result = db.search(q.stamp >= 0)

        if len(lst_result) == 0:
            return 0
        
        return lst_result[0]["stamp"]
    

def write_ts():
    ts = time.time()
    with get_db() as db:
        db.truncate()
        db.insert({'stamp': ts})


def too_recent(span_seconds):
    if time.time() >= get_ts() + span_seconds:
        return False
    return True
    

#print(get_ts())
#write_ts()
#print(get_ts())
