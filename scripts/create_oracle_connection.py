"""
Create and test an Oracle DB connection for this project.
This script will:
- Create a `.env` file with the provided connection settings
- Attempt to connect using `oracledb` and report success/failure

Usage (from project root):
    python scripts/create_oracle_connection.py

Note: Ensure project dependencies are installed and any system policies
allow running the Python interpreter from your virtualenv.
"""
import os
from getpass import getpass

DEFAULTS = {
    'ORACLE_CONNECTION_NAME': 'Application development database',
    'ORACLE_USER': 'Stamford',
    'ORACLE_PASSWORD': 'stamford123',
    'ORACLE_HOST': 'localhost',
    'ORACLE_PORT': '1521',
    'ORACLE_SERVICE': 'xepdb1'
}

ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')


def write_env(env_path, values):
    lines = [f"{k}={v}\n" for k, v in values.items()]
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"Wrote environment file: {env_path}")


def try_connect(values):
    try:
        import oracledb
    except Exception as e:
        print(f"Cannot import oracledb: {e}")
        print("Install requirements: pip install -r requirements.txt")
        return False

    try:
        # Try thin-mode connect first (host, port, service_name)
        conn = oracledb.connect(
            user=values['ORACLE_USER'],
            password=values['ORACLE_PASSWORD'],
            host=values['ORACLE_HOST'],
            port=int(values['ORACLE_PORT']),
            service_name=values['ORACLE_SERVICE']
        )
        conn.close()
        print("Successfully connected to Oracle using provided settings.")
        return True
    except Exception as e:
        print(f"Failed to connect to Oracle: {e}")
        return False


def main():
    print("Create Oracle connection for this project")
    print("Press Enter to accept the default shown in []")

    values = {}
    for k, default in DEFAULTS.items():
        prompt = f"{k} [{default}]: "
        val = input(prompt).strip()
        values[k] = val if val else default

    # For safety, allow confirming password interactively
    if not values.get('ORACLE_PASSWORD'):
        values['ORACLE_PASSWORD'] = getpass('ORACLE_PASSWORD: ')

    write_env(ENV_PATH, values)

    print('\nAttempting to connect to Oracle with these values...')
    try_connect(values)


if __name__ == '__main__':
    main()
