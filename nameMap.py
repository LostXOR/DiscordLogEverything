# Map to convert names for arrays and dicts of objects into their actual type
# For example, an array named "attachments" contains type "attachment", and needs to be converted accordingly
# Similarly, a dict named "author" contains type "user", so the same must be done
nameMap = {
    "mentions": "user",
    "author": "user",
    "roles": "role",
    "components": "component",
    "embeds": "embed",
    "attachments": "attachment"
}