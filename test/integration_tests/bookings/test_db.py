from datetime import date
from src.schemas.bookings import BookingsAdd, BookingsPATCH


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingsAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100,
    )
    # TO CRUD

    create_booking = await db.bookings.add(booking_data)
    assert create_booking is not None
    assert create_booking.price == 100

    booking_id = create_booking.id

    # Read
    found = await db.bookings.get_one_or_none(id=booking_id)
    assert found is not None
    assert found.user_id == user_id

    # Update
    update_data = BookingsPATCH(
        date_to=date(year=2024, month=8, day=25),
        price=200,
    )
    await db.bookings.edit(update_data, id=booking_id, exclude_unset=True)
    update_booking_data = await db.bookings.get_one_or_none(id=booking_id)

    assert update_booking_data.price == 200
    assert update_booking_data.user_id == user_id
    assert update_booking_data.date_to == date(year=2024, month=8, day=25)

    # delete
    delete_bookings = await db.bookings.delete(id=booking_id)
    assert delete_bookings is None

    await db.commit()
