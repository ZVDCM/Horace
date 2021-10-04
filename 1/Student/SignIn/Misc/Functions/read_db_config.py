from configparser import ConfigParser
from SignIn.Misc.Functions.relative_path import relative_path


def read_db_config():
    path = relative_path('Config', [''], 'client.ini')

    parser = ConfigParser()
    parser.read(path)

    db = {}
    if parser.has_section('client'):
        items = parser.items('client')

        for item in items:
            db[item[0]] = item[1]

    else:
        raise Exception(f'client not found in the client.ini file')

    return db
