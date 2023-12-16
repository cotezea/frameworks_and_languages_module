from typing import List, Optional
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models import Item, ItemCreate, Location, DateRange
from datetime import datetime
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

items_id_counter = 1
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
    item_id = str(items_id_counter)
    new_item = Item(id=item_id, date_from=datetime.now().isoformat(), **item.dict())
    items[item_id] = new_item
    items_id_counter += 1
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

@app.exception_handler(status.HTTP_422_UNPROCESSABLE_ENTITY)
async def validation_exception_handler(request, exc):
    error_msg = verify_item_create(request.json())
    if error_msg:
        content = {"message": "Validation error", "details": error_msg}
    else:
        content = {"message": "Method not allowed"}
    return JSONResponse(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED if error_msg else status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=content
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)