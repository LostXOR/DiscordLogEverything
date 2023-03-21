import uuid, time, globalVars

def logEvent(eventType, eventData = []):
    rowUUID = str(uuid.uuid4())
    newRow = [rowUUID, time.time()] + eventData
    parameters = ", ".join("?" * len(newRow))
    globalVars.cursor.execute(f"INSERT INTO Event{eventType} VALUES ({parameters})", newRow)
    return rowUUID