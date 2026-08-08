from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Sports Teams API")


class Team(BaseModel):
    id: int
    name: str
    city: str
    sport: str


class TeamCreate(BaseModel):
    name: str = Field(min_length=1)
    city: str = Field(min_length=1)
    sport: str = Field(min_length=1)


teams = [
    Team(id=1, name="Suns", city="Phoenix", sport="Basketball"),
    Team(id=2, name="Diamondbacks", city="Phoenix", sport="Baseball"),
    Team(id=3, name="Vikings", city="Minnesota", sport="Football"),
    Team(id=4, name="Red Wings", city="Detroit", sport="Hockey"),
]


@app.get("/teams", response_model=list[Team])
def get_teams():
    return teams


@app.get("/teams/{team_id}", response_model=Team)
def get_team(team_id: int):
    for team in teams:
        if team.id == team_id:
            return team
    raise HTTPException(status_code=404, detail="Team not found")


@app.post("/teams", response_model=Team, status_code=201)
def create_team(new_team: TeamCreate):
    next_id = max(team.id for team in teams) + 1
    team = Team(
        id=next_id,
        name=new_team.name,
        city=new_team.city,
        sport=new_team.sport,
    )
    teams.append(team)
    return team
