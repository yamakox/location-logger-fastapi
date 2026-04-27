from sqlmodel import create_engine
from ..common import env

# MARK: create engine

engine_url = f'mysql+pymysql://{env.DB_USER}:{env.DB_PASSWORD}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}'
engine = create_engine(engine_url, echo=env.ENGINE_ECHO)
