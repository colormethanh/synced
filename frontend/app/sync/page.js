"use client";
import React, { useState, useEffect } from 'react'
export default function SyncCalendarPage() {
  const [authUrl, setAuthUrl] = useState(null);
  const [isAuthorized, setIsAuthorized] = useState(false);

  function syncCalendar() {
    try {
        console.log("Fetching Calendar")
        fetch('http://localhost:8000/calendar', {
              credentials: 'include'
            })
        .then(res => res.json())
        .then(data => console.log(data))
    } catch (err) {
      console.log(err)
    }
  }


  useEffect(() => {
    // Check the status of our auth token
    // If the access token is present, no need to sync
    // If the auth token is not present grab the authURL
    try {
      fetch('http://localhost:8000/auth/status', {
              credentials: 'include'
            })
        .then(res => res.json())
        .then(data => {
          console.log("Checking auth status")
          console.log(data)
          if(!data.authenticated){
            console.log(`user is not authenticated ${data}`)
            fetch('http://localhost:8000/auth/google', {
              credentials: 'include'
            })
              .then((res) => res.json())
              .then((data) => {
                setAuthUrl(data.auth_url)
              }); 
          } else {
            setIsAuthorized(true)
          }
        });
    } catch (error) {
      console.log(error)
    }
  }, []);


  return (
    <main>
      <h1> Google Calendar Integration </h1>
      {authUrl && (
        <a href={authUrl}>
          <button>Connect Google Calendar</button>
        </a>
      )}
      {
        isAuthorized &&
        <>
        <div style={{'width': '10rem', 'height': '2.5rem', 'backgroundColor':'green' , 'border': '2px solid white'}}>
          You are Authorized
        </div>

        <button 
          onClick={syncCalendar}
          style={{'marginTop': '1rem'}}
          >
          Sync Your Calendar
        </button>
        </>
      }
    </main>
  )
}
