from sqlalchemy.orm import Session
from models import Participant, Emoji

def seed_data(db: Session):
    if db.query(Participant).count() > 0:
        return

    participants = [
        "Deborah", "Gabriel", "Daniel", "Katy",
        "Maria Eduarda", "Ju", "Maria",
        "Sandro", "Ritchele"
    ]

    for name in participants:
        db.add(Participant(name=name))

    emojis = [
        ("🌅", "Good Vibes", 1),
        ("🍻", "Parceiro(a)", 1),
        ("👑", "Líder do Dia", 2),
        ("⏰", "Atrasado(a)", -1),
        ("😴", "Dorminhoco(a)", -1),
        ("💸", "Gastador(a)", -1),
    ]

    for icon, name, points in emojis:
        db.add(Emoji(icon=icon, name=name, points=points))

    db.commit()