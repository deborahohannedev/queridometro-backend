from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from contextlib import asynccontextmanager

from database import SessionLocal, engine
import models
import schemas
from seed import seed_data
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db = SessionLocal()
    seed_data(db)
    db.close()

    yield

    # Shutdown (se quiser algo depois)

app = FastAPI(
    title="Queridômetro Trip Edition",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://SEU-FRONT.vercel.app"],  # para MVP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/participants")
def list_participants(db: Session = Depends(get_db)):
    return db.query(models.Participant).all()

@app.get("/emojis")
def list_emojis(db: Session = Depends(get_db)):
    return db.query(models.Emoji).all()

@app.post("/vote")
def create_vote(vote: schemas.VoteCreate, db: Session = Depends(get_db)):
    if vote.voter_id == vote.target_id:
        raise HTTPException(status_code=400, detail="Não pode votar em si mesmo")

    db_vote = models.Vote(**vote.dict())
    db.add(db_vote)
    db.commit()

    return {"message": "Voto registrado com sucesso"}

@app.get("/ranking")
def ranking(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT p.name, COALESCE(SUM(e.points), 0) as score
        FROM participants p
        LEFT JOIN votes v ON v.target_id = p.id
        LEFT JOIN emojis e ON e.id = v.emoji_id
        GROUP BY p.name
        ORDER BY score DESC
    """))

    return [{"name": row[0], "score": row[1]} for row in result]
