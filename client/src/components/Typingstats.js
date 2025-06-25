import React, { useEffect, useState } from "react";
import io from "socket.io-client";
import "./TypingStats.css"; // You’ll create this for styles

const socket = io("http://localhost:5000");

const TypingStats = () => {
  const [startTime, setStartTime] = useState(null);
  const [typed, setTyped] = useState("");
  const [wpm, setWpm] = useState(0);

  useEffect(() => {
    if (typed.length === 1) {
      setStartTime(Date.now());
    }

    if (typed.length > 1 && startTime) {
      const now = Date.now();
      const minutes = (now - startTime) / 60000;
      const words = typed.trim().split(" ").length;
      const currentWpm = Math.round(words / minutes);
      setWpm(currentWpm);

      // Emit to backend
      socket.emit("progress", { typed, wpm: currentWpm });
    }
  }, [typed]);

  useEffect(() => {
    socket.on("progress_update", (data) => {
      console.log("Server broadcast:", data);
    });

    return () => socket.off("progress_update");
  }, []);

  return (
    <div className="typing-container">
      <h2>Typing Speed Tracker</h2>
      <textarea
        value={typed}
        onChange={(e) => setTyped(e.target.value)}
        placeholder="Start typing..."
        rows={5}
      />
      <div className="stats">
        <p><strong>WPM:</strong> {wpm}</p>
        <progress value={wpm} max="120" />
      </div>
    </div>
  );
};

export default TypingStats;
