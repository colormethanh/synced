# Synced

An app focused on streamlining the planning of events by syncing group member's Calendars into one centralized calendar to better view when people are available. 

## The Stack
Frontend:
- Next.js react framework
- CSS

Backend: 
- Fast Api
- Python

## Quick Start

### Starting the backend
1. cd in backend 
2. Start a virtual env. <br>
`python -m venv myvenv` <br>
You'll need to figure out how to activate a venv based on your OS
3. CD into the backend with... <br> `cd backend` 
4. Install required packages in the requirement.txt file by running <br>
`pip install -r requirements.txt`
5. Start the backend server by running <br>
`uvicorn main:app --reload --port 8000`

### Starting the frontend
1. Cd into the frontend folder <br>
`cd fronend`
2. Install dependencies
`npm install`
3. Start the frontend server
`npm run dev`

### Set up env Variables
The env variable values can be found in the shared notion. 

The frontend and backend should have separate .env files. I think that's the easiest and less confusing way to setting it up. 

**Note On env. Variables with next.js** <br>
Next.js env variables must be appended with <em>NEXT_PUBLIC_</em> followed by the name of your env name <br>
ex. NEXT_PUBLIC_SUPER_SECRET_ID=supersecretidnottobesharedwithotherpeeople
