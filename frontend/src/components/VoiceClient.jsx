import { useState, useRef, useEffect } from "react";
import {
    connect,
    disconnect,
    sendAudio,
    sendUtteranceEnd,
    isConnected,
} from "../services/websocket";
import PCMRecorder from "../audio/pcmRecorder";

export default function VoiceClient() {
    const [connected, setConnected] = useState(false);
    const [recording, setRecording] = useState(false);
    const [messages, setMessages] = useState([]);

    const recorderRef = useRef(null);
    
    // Keeps a fresh reference of startRecording for the event listener
    const startRecordingRef = useRef(null);

    const connectSocket = () => {
        if (isConnected()) return;
        connect((msg) => {
            setMessages((prev) => [...prev, msg]);
        });
        setConnected(true);
    };

    const disconnectSocket = () => {
        disconnect();
        setConnected(false);
    };

    const startRecording = async () => {
        if (recording) return;

        if (!isConnected()) {
            alert("Connect first");
            return;
        }

        const recorder = new PCMRecorder((pcm) => {
            sendAudio(pcm);
        });

        recorderRef.current = recorder;

        await recorder.start();

        setRecording(true);

        setMessages(prev => [
            ...prev,
            "🎤 Recording started",
        ]);
    };

    // Update the mutable reference whenever startRecording changes
    startRecordingRef.current = startRecording;

    const stopRecording = async () => {
        if (!recorderRef.current) return;

        await recorderRef.current.stop();

        recorderRef.current = null;

        sendUtteranceEnd();

        setRecording(false);

        setMessages(prev => [
            ...prev,
            "🛑 Recording stopped",
        ]);
    };

    // Listen for the CustomEvent to trigger auto-re-listening
    useEffect(() => {
        const handler = () => {
            console.log("🎤 Restart Listening");
            if (startRecordingRef.current) {
                startRecordingRef.current();
            }
        };

        window.addEventListener("ai-finished", handler);

        return () => {
            window.removeEventListener("ai-finished", handler);
        };
    }, []);

    return (
        <div style={{ marginTop: 20 }}>
            <button onClick={connected ? disconnectSocket : connectSocket}>
                {connected ? "Disconnect" : "Connect"}
            </button>
            {" "}
            <button disabled={!connected || recording} onClick={startRecording}>
                🎤 Start Talking
            </button>
            {" "}
            <button disabled={!recording} onClick={stopRecording}>
                Stop
            </button>
            <hr />
            <div
                style={{
                    height: 250,
                    overflowY: "auto",
                    border: "1px solid gray",
                    padding: 10,
                }}
            >
                {messages.map((m, i) => (
                    <div key={i}>
                        {typeof m === "object" ? JSON.stringify(m) : m}
                    </div>
                ))}
            </div>
        </div>
    );
}
