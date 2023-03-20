import uuid, time, gb

# Used to update deleted objects to represent that they are deleted
def deleteObject(objectID, objectType, eventUUID):
    gb.cursor.execute(f"INSERT INTO {objectType} (uuid, timestamp, deleted, event_uuid, id) VALUES (?, ?, ?, ?, ?)", [str(uuid.uuid4()), time.time(), 1, eventUUID, objectID])