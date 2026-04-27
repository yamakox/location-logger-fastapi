from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.environ.get('DB_NAME', 'lldb')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = eval(os.environ.get('DB_PORT', '3306'))
DB_USER = os.environ.get('DB_USER', 'DBUser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'DBPassword')
ENGINE_ECHO = eval(os.environ.get('ENGINE_ECHO', 'False'))
FRONTEND_ORIGIN = os.environ.get('FRONTEND_ORIGIN', '')
