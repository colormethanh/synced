"use client";
import React, { useState, useEffect } from 'react'
export default function SyncCalendarPage() {
  const [authUrl, setAuthUrl] = useState(null);
  const [isAuthorized, setIsAuthorized] = useState(false);



  useEffect(() => {
    // Check the status of our auth token
    // If the access token is present, no need to sync
    // If the auth token is not present grab the authURL

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
        <div style={{'width': '10rem', 'height': '2.5rem', 'backgroundColor':'green' , 'border': '2px solid white'}}>
          You are Authorized
        </div>
      }
    </main>
  )
}
