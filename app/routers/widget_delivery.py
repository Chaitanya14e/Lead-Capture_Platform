from pathlib import Path

from fastapi import APIRouter, Query
from fastapi.responses import Response

router = APIRouter(tags=["Widget Delivery"])

WIDGET_JS_PATH = Path(__file__).resolve().parent.parent / "widget.js"

WIDGET_VERSION = "1.0.0"


@router.get("/widget.js")
def get_widget_js(
    version: str | None = Query(default=None)
):
    javascript = WIDGET_JS_PATH.read_text(encoding="utf-8")

    requested_version = version or WIDGET_VERSION

    return Response(
        content=javascript,
        media_type="application/javascript",
        headers={
            "Cache-Control": "public, max-age=300",
            "ETag": f'"widget-{requested_version}"',
            "X-Widget-Version": requested_version,
        },
    )