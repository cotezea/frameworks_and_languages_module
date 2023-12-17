from fastapi import FastAPI, HTTPException, Response, status, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from models import Item, ItemCreate
from datetime import datetime
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

items = {}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<html><body><h1>FreeCycle API</h1></body></html>"

def verify_item_create(item: dict) -> Optional[str]:
    try:
        ItemCreate(**item)
        return None
    except Exception as e:
        return str(e)

@app.post("/item/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    item_id = str(uuid.uuid4())
    new_item = Item(id=item_id, date_from=datetime.now().isoformat(), **item.dict())
    items[item_id] = new_item
    return new_item

@app.get("/item/{item_id}/", response_model=Item)
async def get_item(item_id: str):
    item = items.get(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

@app.delete("/item/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: str):
    if item_id in items:
        del items[item_id]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/items/", response_model=List[Item])
async def get_all_items():
    return list(items.values())

@app.options("/")
async def options_root() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT, headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS, DELETE",
    })

@app.options("/item/")
async def options_item() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT, headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, DELETE, OPTIONS",
    })

@app.options("/items/")
async def options_items() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT, headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
    })

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        content=jsonable_encoder({"detail": exc.errors()}),
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)