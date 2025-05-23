"use client";

import React, { useEffect, useState } from 'react'

export default function HelloWorldPage() {
  const [message, setMessage] = useState("")


  useEffect(() => {
    fetch("http://localhost:8000/api/hello")
    .then(res => res.json())
    .then(data => setMessage(data.message))
    .catch(err => console.error(err))
  }, [])


  return (
    <h1>{message || "Loading"}</h1>
  )
}
