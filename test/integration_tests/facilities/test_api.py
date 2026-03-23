async def test_add_facility(ac):
    response = await ac.post("/facilities", json={"title": "Wi-fi"})

    assert response.status_code == 200
    assert response.json()["falities"]["title"] == "Wi-fi"
    assert isinstance(response.json(), dict)


async def test_get_facilities(ac):
    response = await ac.get("/facilities")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
