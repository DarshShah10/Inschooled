// src/App.js
import React, { useState } from "react";
import RoadmapForm from "./components/RoadmapForm";
import Chat from "./components/Chat";
import "./App.css";

function App() {
  const [roadmap, setRoadmap] = useState("");
  const [sessionId, setSessionId] = useState(null);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Roadmap Chatbot</h1>
      </header>
      {!roadmap && !sessionId && (
        <RoadmapForm setRoadmap={setRoadmap} setSessionId={setSessionId} />
      )}
      {roadmap && sessionId && <Chat roadmap={roadmap} sessionId={sessionId} />}
    </div>
  );
}

export default App;
