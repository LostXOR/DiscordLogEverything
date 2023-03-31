import uuid, globalVars
from nameMap import nameMap

# Saves a JSON object to the database
def saveObject(objectJSON, objectType, parentUUID, timestamp, deleted):
    selfUUID = str(uuid.uuid4())

    objectKeys = list(objectJSON.keys());
    objectValues = []
    # Iterate through each key in the JSON
    for key in objectKeys:
        value = objectJSON[key]
        # Look up type in name map
        mappedName = nameMap[objectType][key] if objectType in nameMap and key in nameMap[objectType] else key

        # If value is a type that can be added to the database, add it to the database
        if isinstance(value, (str, int, float, bool, type(None))):
            objectValues.append(value)

        # If value is an array of a type that can be added to the database, add a comma-separated list to the database
        # May cause issues if there are commas in the data, must look into later
        elif isinstance(value, list) and (len(value) == 0 or isinstance(value[0], (str, int, float, bool, type(None)))):
            objectValues.append(",".join(map(str, value)) if value else None)

        # If value is a dict, save it with this function and add the UUID to the database
        elif isinstance(value, dict):
            childUUID = saveObject(value, mappedName, selfUUID, timestamp, deleted)
            objectValues.append(childUUID)

        # If value is an array of dicts, save each element with this function and add a comma-separated list of UUIDs to the database
        elif isinstance(value, list) and (len(value) == 0 or isinstance(value[0], dict)):
            childUUIDs = []
            for element in value:
                childUUIDs.append(saveObject(element, mappedName, selfUUID, timestamp, deleted))
            objectValues.append(",".join(childUUIDs) if childUUIDs else None)

        # PANIC!!!!
        else:
            print(f"PANIC!!!! Non-saveable object: {type(value).__name__}")
            objectValues.append(None)

    # Dynamically create a table with a column for each key in the data
    globalVars.cursor.execute(f"CREATE TABLE IF NOT EXISTS {objectType}(uuid PRIMARY KEY, parent_uuid, timestamp, deleted)")
    for key in objectKeys:
        try:
            globalVars.cursor.execute(f"ALTER TABLE {objectType} ADD COLUMN {key}")
        except:
            pass

    # Write data to database
    # keyString could be subject to SQL injection but all values are provided by Discord so almost certainly not
    # Unfortunately column names cannot be parameterized so this is unavoidable
    keyString = ", ".join(["uuid", "parent_uuid", "timestamp", "deleted"] + objectKeys)
    parameterString = ", ".join(["?"] * (len(objectValues) + 4))
    globalVars.cursor.execute(f"INSERT INTO {objectType} ({keyString}) VALUES ({parameterString})", [selfUUID, parentUUID, timestamp, deleted] + objectValues)
    globalVars.database.commit()

    return selfUUID