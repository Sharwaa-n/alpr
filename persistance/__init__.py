from .models import User, DetectionRequest, Detection, Plate, LostClaim
from .utils.DB import db


def initDb():
    if not db.connection:
        db.connect()
    db.create_tables([User, DetectionRequest, Detection, Plate, LostClaim])