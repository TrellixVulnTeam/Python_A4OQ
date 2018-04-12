
from .db_manager import SaveSQL

ImpalaConnect = 'DRIVER={Cloudera ODBC Driver for Impala};HOST=testalarmodbc;PORT=21050'
rundata = ""

def get_dig_metric_data(shift_start_timestamp):
    """
        get dig metric data from impala.
    """
    result = []
    query = r"select dump_start_ang ,dump_start_tooth_extension from dwh.es_cycles where cycle_type=1"
    query_statement = r" and shift_start_timestamp = {0}"
    if shift_start_timestamp is not None:
        query = query + query_statement.format(shift_start_timestamp)
    db = __construct_DB()
    records = db.readData(query)
    result = records
    return result

def get_dig_path_data(equipment):
    """
        get dig path data from impala.
    """
    result = []
    query = r"select tooth_x ,tooth_y,tooth_z from dwh.es_dig_facts where asset_id='{0}' limit 3000"

    query = query.format(equipment)
    db = __construct_DB()
    records = db.readData(query)
    result = records
    return result

def __construct_DB():
        """
            used for generate the DB connection.
        """
        db = SaveSQL()
        db.setConnectString(ImpalaConnect)

        return db
        

