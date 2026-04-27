from typing import Annotated
from fastapi import (
    APIRouter, HTTPException, Cookie, Header, Response
)
from sqlmodel import Session, select
from ...common.client import setup_client
from ...db.engine import engine
from ...db.model import Client, Location

maxLogCount = 300

def create_router() -> APIRouter:
    # MARK: /api/v1/location
    router = APIRouter(prefix='/location')

    # MARK: 位置情報の一覧を取得する
    @router.get('/')
    def index(
        response: Response, 
        cid: Annotated[str|None, Cookie()] = None, 
        user_agent: Annotated[str|None, Header()] = None, 
    ):
        """位置情報の一覧を取得する。"""
        try:
            with Session(engine) as session:
                client = setup_client(session, response, cid, user_agent)
                statement = (
                    select(Client)
                    .where(Client.cid == client.cid)
                )
                client = session.exec(statement).first()
                if not client:
                    return []
                statement = (
                    select(Location)
                    .where(Location.client_id == client.id)
                    .order_by(Location.timestamp.desc())
                    .limit(maxLogCount)
                )
                locations = session.exec(statement).all()
                return locations
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # MARK: 位置情報を追加する
    @router.post('/')
    def store(
        location: Location, 
        response: Response, 
        cid: Annotated[str|None, Cookie()] = None, 
        user_agent: Annotated[str|None, Header()] = None, 
    ):
        try:
            with Session(engine) as session:
                client = setup_client(session, response, cid, user_agent)
                location.client_id = client.id
                session.add(location)
                session.commit()
                return dict[str, str](id=str(location.id))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
