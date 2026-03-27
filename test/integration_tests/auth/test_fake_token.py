


async def test_user_with_fake_token(authenticated_ac,db):
    # fake_user = {"email": "fake_token@kot.com",
    #              "password": "12345"}
    # await ac.post(
    #     "/auth/register",
    #     json=fake_user
    # )
    # resp_login = await ac.post(
    #     "/auth/login",
    #     json=fake_user
    # )

    token = authenticated_ac.cookies["access_token"]
    header, payload, signature = token.split(".")
    fake_token = f"{header}.{payload}FAKE.{signature}"
    print(fake_token)
    authenticated_ac.cookies.clear()
    print(authenticated_ac.cookies)
    authenticated_ac.cookies["access_token"] = fake_token

    response = await authenticated_ac.get("/auth/me")
    assert response.status_code == 401

    authenticated_ac.cookies.clear()
    authenticated_ac.cookies["access_token"] = token