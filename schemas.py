from pydantic import BaseModel

class VoteCreate(BaseModel):
    voter_id: int
    target_id: int
    emoji_id: int
    day_number: int