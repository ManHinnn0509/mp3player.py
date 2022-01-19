import json

def readJSON_File(p: str, encoding="utf-8"):
    """
        Reads a json file's content from given path
        None will be returned if exception caught
    """
    try:
        with open(p, "r", encoding=encoding) as f:
            return json.load(f)
    except Exception as e:
        # print(e)
        return None