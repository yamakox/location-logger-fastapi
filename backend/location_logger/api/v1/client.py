from typing import Annotated
from fastapi import (
    APIRouter, HTTPException, Cookie, Header, Response
)
from sqlmodel import Session, SQLModel
from ...common.client import setup_client
from ...db.engine import engine

# MARK: ClientResponse
class ClientResponse(SQLModel, table=False):
    cid: str

def create_router() -> APIRouter:
    # MARK: /api/v1/client
    router = APIRouter(prefix='/client')

    # MARK: 位置情報のクライアントを識別するCIDを取得する
    @router.get('/')
    def index(
        response: Response, 
        cid: Annotated[str|None, Cookie()] = None, 
        user_agent: Annotated[str|None, Header()] = None, 
    ):
        """位置情報のクライアントを識別するCIDを取得する。"""
        try:
            with Session(engine) as session:
                client = setup_client(session, response, cid, user_agent)
                return ClientResponse(cid=client.cid)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
