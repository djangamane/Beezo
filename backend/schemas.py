
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class PlayerBase(BaseModel):
    name: str
    position: str
    height: str
    weight: int

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    team_id: int

    class Config:
        orm_mode = True

class TeamBase(BaseModel):
    name: str

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    players: List[Player] = []

    class Config:
        orm_mode = True

class ScoutingReport(BaseModel):
    team_name: str
    executive_summary: str
    opponent_overview: Dict[str, Any]
    key_players: List[Dict[str, Any]]
    coaching_strategy: Dict[str, Any]
    game_day_factors: Dict[str, Any]
    nil_roster_dynamics: str
    warrior_mentality_focus: str
    hoopr_data: str
    torvik_data: str
