from fastapi import FastAPI, Query, Body
import uvicorn
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

app = FastAPI()


hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 2, 'title': 'Dubai', 'name': 'dubai'},
]

def update_hotel(db,id,title,name):
    for hotel in db:
        if hotel['id'] == id:
            if title:
                hotel['title'] = title
            if name:
                hotel['name'] = name
            return hotels
    return None

@app.get('/hotels')
def get_hotels(
        id: int | None = Query(None, description='Id'),
        title: str | None = Query(None, description='Hotel name')
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    return hotels_

@app.post('/hotels')
def create_hotel(
        title : str = Body(embed=True)):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': title
    })
    return {'status': 'Ok'}


@app.delete('/hotels/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}

@app.put("/hotels/{hotel_id}")
def change_hotel(
        hotel_id : int,
        title : str = Body(embed=True),
        name : str = Body(embed=True)
):
    global hotels
    up_hotels = update_hotel(hotels, hotel_id, title, name)
    if up_hotels:
        hotels = up_hotels
        return {'status': 'OK'}
    return {'status': 'Id not found'}


@app.patch("/hotels/{hotel_id}")
def change_hotel_element(
        hotel_id : int,
        title : str | None = Body(None, embed=True),
        name : str | None = Body(None, embed=True)
):
    global hotels
    up_hotels = update_hotel(hotels, hotel_id, title, name)
    if up_hotels:
        hotels = up_hotels
        return {'status': 'OK'}
    return {'status' : 'Id not found'}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)