from sqlalchemy.orm import Session
from models import Participant, Emoji


def clear_data(db: Session):
    db.query(Participant).delete()
    db.query(Emoji).delete()
    db.commit()

def seed_data(db: Session):
    # Limpa tudo antes
    clear_data(db)
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
        ("😶", "Fala demais", -1),
        ("🥱", "Chato(a)", -2),
        ("🏃‍♂️", "Forinha", -1),
        ("🥳", "Inimigo do fim", 2),
        ("🪴", "Planta", -2),
        ("👥", "Boa companhia", 2),
        ("💣", "Fora da viagem", -3),
    ]

    for icon, name, points in emojis:
        existing = db.query(Emoji).filter_by(icon=icon).first()

        if existing:
            # Atualiza se mudar descrição ou pontos
            existing.name = name
            existing.points = points
    else:
        db.add(Emoji(icon=icon, name=name, points=points))

    db.commit()
