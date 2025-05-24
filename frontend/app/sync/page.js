"use client";

import React, { useState, useEffect } from 'react'

export default function SyncCalendarPage() {
  const [authUrl, setAuthUrl] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/auth/google')
      .then((res) => res.json())
      .then((data) => {
        console.log(data)
        setAuthUrl(data.auth_url)
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
    </main>
  )
}
