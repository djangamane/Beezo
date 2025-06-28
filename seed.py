
from sqlalchemy.orm import Session

from backend import crud, schemas
from backend.database import SessionLocal, engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Add teams
teams = [
    schemas.TeamCreate(name="Arizona"),
    schemas.TeamCreate(name="UCLA"),
    schemas.TeamCreate(name="Oregon"),
    schemas.TeamCreate(name="USC"),
    schemas.TeamCreate(name="Stanford")
]

for team in teams:
    crud.create_team(db=db, team=team)

# Add players
players = [
    schemas.PlayerCreate(name="Caleb Love", position="G", height="6-4", weight=205),
    schemas.PlayerCreate(name="Oumar Ballo", position="C", height="7-0", weight=260),
    schemas.PlayerCreate(name="Pelle Larsson", position="G", height="6-6", weight=215),
]

for player in players:
    crud.create_player(db=db, player=player, team_id=1) # Arizona

db.close()

print("Database seeded with sample data.")
