# growing_competency

Small REST API I built using Python and FastAPI to practice API testing. 
The project goal is to keep alist of sport teams in memory and the API will let you look at teams or add a new one using Postman to test it. 

commands to run project

(inside correct dir) 

Terminal 1:

python3 -m venv venv
source venv/bin/active (im on mac)
pip install -r requirements.txt

Start the server: uvicorn main:app --reload

Terminal 2:

(inside correct dir) 

source venv/bin/activate
pytest -v

This will run the automated tests

----

Endpoints I implemented include 

GET /teams

GET /teams/{team_id}

POST /teams


