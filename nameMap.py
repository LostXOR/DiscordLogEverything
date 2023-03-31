# Map to convert names for arrays and dicts of objects into their actual type
# For example, an array named "attachments" in a message contains type "attachment", and needs to be converted accordingly
# Similarly, a dict named "author" in a message contains type "user", so the same must be done
nameMap = {
    "message": {
        "mentions": "user",
        "author": "user",
        "roles": "role",
        "components": "component",
        "embeds": "embed",
        "attachments": "attachment"
    },
    "hashes": {
        "roles": "hash",
        "metadata": "hash",
        "channels": "hash"
    },
    "guild_hashes": {
        "roles": "hash",
        "metadata": "hash",
        "channels": "hash"
    },
    "channel": {
        "permission_overwrites": "permission_overwrite"
    }
}