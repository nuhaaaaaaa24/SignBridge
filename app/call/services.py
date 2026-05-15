"""Helper utilities for call-room management.

Provides room code generation and uniqueness guarantees used by the
:func:`~app.call.routes.create_room` view when a new
:class:`~app.models.Room` is created.
"""

import random
import string

import sqlalchemy as sa

from app.models import Room
from extensions import db


def generate_room_code():
    """Generate a random room code in ``XXXX-0000`` format.

    Produces a code consisting of four random uppercase ASCII letters,
    a hyphen, and four random decimal digits. The format is chosen to
    be short enough to communicate verbally or type manually while
    providing a large enough space (26⁴ × 10⁴ = 4,569,760,000
    combinations) to make collision and brute-force enumeration
    unlikely in practice.

    Returns:
        str: A random code in the form ``"ABCD-1234"``.

    Example:
        ::

            >>> generate_room_code()
            'KRTW-4921'
    """
    letters = ''.join(random.choices(string.ascii_uppercase, k=4))
    numbers = ''.join(random.choices(string.digits, k=4))
    return f"{letters}-{numbers}"


def generate_unique_room_code():
    """Return a room code that does not already exist in the database.

    Calls :func:`generate_room_code` in a loop, querying the
    :class:`~app.models.Room` table after each attempt until a code is
    found that has no matching row. Given the size of the code space,
    more than one iteration is vanishingly unlikely under any realistic
    load.

    Note:
        This function performs at least one database query per call and
        must be invoked within an active Flask application context.
        A small TOCTOU race exists between the uniqueness check and the
        subsequent ``INSERT`` in the caller; the
        :attr:`~app.models.Room.room_code` column should carry a
        ``UNIQUE`` constraint so the database enforces uniqueness as a
        final safety net.

    Returns:
        str: A room code in the form ``"XXXX-0000"`` that is not
        currently present in the :class:`~app.models.Room` table.
    """
    while True:
        code = generate_room_code()
        exists = db.session.scalar(
            sa.select(Room).where(Room.room_code == code)
        )
        if not exists:
            return code