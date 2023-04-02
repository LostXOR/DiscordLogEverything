import uuid, json, globalVars

# Writes a JSON object to the database
def writeObject(object, objectType, socketRecvUUID, timestamp, deleted = False):
    row = [str(uuid.uuid4()), socketRecvUUID, timestamp, objectType, deleted, json.dumps(object)]
    globalVars.cursor.execute(f"INSERT INTO object VALUES (?, ?, ?, ?, ?, ?)", row)
    globalVars.database.commit()