from fastapi import APIRouter, HTTPException, Response
from sqlmodel import SQLModel
from importlib.metadata import version
from ...common.common import set_common_response_header


# MARK: VersionResponse
class VersionResponse(SQLModel, table=False):
    version: str


def create_router() -> APIRouter:
    # MARK: /api/v1/misc
    router = APIRouter(prefix='/misc')

    # MARK: /api/v1/misc/version
    @router.get('/version', response_model=VersionResponse)
    def get_version(response: Response):
        """バージョン情報を取得する。"""
        try:
            set_common_response_header(response)
            return VersionResponse(version=version('location_logger'))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
