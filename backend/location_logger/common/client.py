from fastapi import Response
from sqlmodel import Session, select
import uuid
from ..db.model import Client

# MARK: クライアントのリクエストに対してCookieを設定する
def setup_client(session: Session, response: Response, cid: str|None, ua: str|None) -> Client:
    if client := _get_client(session, cid):
        return client
    client = _create_client(session, ua)
    response.set_cookie(key='cid', value=client.cid)
    return client

# MARK: 該当するClientを取得する (cidのNoneチェックも同時に行う)
def _get_client(session: Session, cid: str|None) -> Client|None:
    if cid is None:
        return None
    statement = (
        select(Client)
        .where(Client.cid == cid)
    )
    results = session.exec(statement)
    return results.first()

# MARK: clientsテーブルに新しいクライアントを追加する
def _create_client(session: Session, ua: str|None) -> Client:
    for i in range(5):
        cid = str(uuid.uuid4())
        if _get_client(session, cid) is None:
            client = Client(cid=cid, ua=ua)
            session.add(client)
            session.commit()
            return client
    else:
        raise Exception('Cookieに渡す識別情報の割り当てに失敗しました。')
