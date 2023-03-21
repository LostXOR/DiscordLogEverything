import uuid, time, globalVars

# Used to update deleted objects to represent that they are deleted
def deleteObject(objectID, objectType, eventUUID):
    globalVars.cursor.execute(f"INSERT INTO {objectType} (uuid, timestamp, deleted, event_uuid, id) VALUES (?, ?, ?, ?, ?)", [str(uuid.uuid4()), time.time(), 1, eventUUID, objectID])