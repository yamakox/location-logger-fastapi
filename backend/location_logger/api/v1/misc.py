from fastapi import APIRouter, HTTPException
from sqlmodel import SQLModel
from importlib.metadata import version

# MARK: VersionResponse
class VersionResponse(SQLModel, table=False):
    version: str

def create_router() -> APIRouter:
    # MARK: /api/v1/misc
    router = APIRouter(prefix='/misc')

    # MARK: /api/v1/misc/version
    @router.get('/version', response_model=VersionResponse)
    def get_version():
        """バージョン情報を取得する。"""
        try:
            return VersionResponse(version=version('location_logger'))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
