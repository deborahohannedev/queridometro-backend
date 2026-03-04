from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

class Emoji(Base):
    __tablename__ = "emojis"

    id = Column(Integer, primary_key=True, index=True)
    icon = Column(String)
    name = Column(String)
    points = Column(Integer)

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    voter_id = Column(Integer, ForeignKey("participants.id"))
    target_id = Column(Integer, ForeignKey("participants.id"))
    emoji_id = Column(Integer, ForeignKey("emojis.id"))
    day_number = Column(Integer)