GET_BODY_URL = """
    SELECT fbx_url
    FROM body_info
    WHERE num = %s
"""

GET_HAIR_URL = """
    SELECT fbx_url
    FROM hair_info
    where num = %s
"""

GET_BODY_CONFIG = """
    SELECT x, y, z, s
    FROM body_info
    WHERE num = %s
"""

GET_HAIR_CONFIG = """
    SELECT x, y, z, s
    FROM hair_info
    WHERE num = %s
"""

