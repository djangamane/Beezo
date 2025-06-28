
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import subprocess
import os

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/teams/", response_model=list[schemas.Team])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teams = crud.get_teams(db, skip=skip, limit=limit)
    return teams

@app.get("/api/players/", response_model=list[schemas.Player])
def read_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    players = crud.get_players(db, skip=skip, limit=limit)
    return players

@app.get("/api/scouting-report/{team_id}", response_model=schemas.ScoutingReport)
def get_scouting_report(team_id: int, db: Session = Depends(get_db)):
    team = crud.get_team(db, team_id=team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    # In a real application, you would have more sophisticated logic here
    # to generate the report based on the team_id.
    # This is a placeholder to demonstrate the structure.
    
    r_script_path = os.path.join(os.getcwd(), "warrior-intel", "data", "r_scripts")

    # Execute R scripts and get output
    try:
        hoopr_output = subprocess.check_output(['Rscript', os.path.join(r_script_path, 'hoopR_script.R'), team.name], text=True)
    except subprocess.CalledProcessError as e:
        hoopr_output = f"Error executing hoopR script: {e}"

    try:
        torvik_output = subprocess.check_output(['Rscript', os.path.join(r_script_path, 'toRvik_script.R'), team.name], text=True)
    except subprocess.CalledProcessError as e:
        torvik_output = f"Error executing toRvik script: {e}"


    # Placeholder data - in a real app, this would be dynamically generated
    executive_summary = f"This is a sample scouting report for {team.name}. They are a strong offensive team with a fast-paced tempo. Key players to watch are their point guard and center."
    opponent_overview = {
        "team_stats": {
            "adj_o": 115.2,
            "adj_d": 95.8,
            "tempo": 72.1,
        },
        "recent_form": "W-W-L-W-W",
        "style_of_play": "Uptempo, focus on 3-point shooting."
    }
    key_players = [
        {
            "name": "Player 1",
            "position": "PG",
            "stats": {"ppg": 18.5, "apg": 6.2, "rpg": 3.1},
            "shot_chart_url": f"https://example.com/shot_chart_{team.name.lower().replace(' ', '_')}_player1.png",
            "tendencies": "Loves to drive left, excellent finisher at the rim."
        },
        {
            "name": "Player 2",
            "position": "C",
            "stats": {"ppg": 15.2, "rpg": 10.8, "bpg": 2.1},
            "shot_chart_url": f"https://example.com/shot_chart_{team.name.lower().replace(' ', '_')}_player2.png",
            "tendencies": "Dominant post player, great rebounder."
        }
    ]
    coaching_strategy = {
        "offensive_sets": "Horns, Flex, Motion",
        "defensive_schemes": "Man-to-man, 2-3 Zone",
        "philosophy": "Defense-first, grind-it-out style."
    }
    game_day_factors = {
        "injuries": "Starting SF is a game-time decision (ankle).",
        "travel_impact": "Team is on the second game of a road trip.",
        "venue_performance": "Slightly worse on the road, especially from the free-throw line."
    }
    nil_roster_dynamics = "Lost their starting point guard to the transfer portal last season, but brought in a high-impact transfer from a smaller conference."
    warrior_mentality_focus = "This team has shown frustration when pressured. We can exploit this by being aggressive on defense and forcing turnovers. Their point guard is known to complain to the refs."


    return schemas.ScoutingReport(
        team_name=team.name,
        executive_summary=executive_summary,
        opponent_overview=opponent_overview,
        key_players=key_players,
        coaching_strategy=coaching_strategy,
        game_day_factors=game_day_factors,
        nil_roster_dynamics=nil_roster_dynamics,
        warrior_mentality_focus=warrior_mentality_focus,
        hoopr_data=hoopr_output.strip(),
        torvik_data=torvik_output.strip()
    )
