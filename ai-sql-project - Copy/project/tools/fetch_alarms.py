from psycopg2 import connect
from psycopg2.extensions import cursor
from strands import tool

def query_many(cursor: cursor, length: int) -> list[dict]:
    columns = [desc[0] for desc in cursor.description] if cursor.description else []
    alarm_tuples = cursor.fetchmany(length)
    alarms = []
    
    for alarm_tuple in alarm_tuples:
        alarm_dict = dict(zip(columns, alarm_tuple))
        alarms.append(alarm_dict)
    return alarms

def fetch_last_alarms(length=1):
    conn = connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password="admin"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alarm ORDER BY alarm_ts DESC")
    
    alarms = query_many(cursor, length)
    
    conn.close()
    return alarms

@tool
def fetch_last_alarm_messages(length="10") -> str:
    """
    Retrieves the latest alarm messages from the database, useful detecting patterns.\n
    Only use this tool if you need it.
    """

    alarms = fetch_last_alarms(int(length))
    alarm_messages = [alarm['alarm_text'] for alarm in alarms]

    return "\n".join(alarm_messages)