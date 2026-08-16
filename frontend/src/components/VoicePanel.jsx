import { useEffect, useRef } from "react";
import { Mic } from "lucide-react";
import { motion } from "framer-motion";

import {
    connect,
    disconnect,
    sendAudio,
    sendUtteranceEnd,
    isConnected,
} from "../services/websocket";

import PCMRecorder from "../audio/pcmRecorder";
import { useVoice } from "../context/VoiceContext";

export default function VoicePanel() {
    const {
        messages,
        setMessages,
        customer,
        setCustomer,
        recording,
        setRecording,
        dgStatus,
        setDgStatus,
        aiSpeaking,
        setAiSpeaking,
        voiceState,
        setVoiceState,
    } = useVoice();

    const recorderRef = useRef(null);

    // Keeps fresh reference of startRecording for the event listener loop
    const startRecordingRef = useRef(null);

    useEffect(() => {
        const connectTimeout = window.setTimeout(() => {
            connect((msg) => {
                console.log("Backend:", msg);

                if (msg.dg_status) {
                    setDgStatus(msg.dg_status);
                    return;
                }

                if (msg.customer) {
                    setCustomer(msg.customer);
                }

                // Step 4 - Updated WebSocket Callback
                if (msg.text) {
                    setMessages(prev => [
                        ...prev,
                        {
                            sender: "AI",
                            text: msg.text,
                        }
                    ]);

                    // If we're currently recording, stop before the AI speaks
                    if (recorderRef.current) {
                        // stopRecording is defined later in the component; call it and swallow errors
                        stopRecording().catch(console.error);
                    }

                    setAiSpeaking(true);
                    setVoiceState("speaking");
                }
            });
        }, 0);

        return () => {
            window.clearTimeout(connectTimeout);
            disconnect();
        };
    }, []);

    const startRecording = async () => {
        if (recording) return;

        if (!isConnected()) {
            alert("Backend is not connected");
            return;
        }

        const recorder = new PCMRecorder((pcm) => {
            sendAudio(pcm);
        });

        recorderRef.current = recorder;

        await recorder.start();

        setRecording(true);
        setVoiceState("listening");
    };

    // Update mutable reference whenever startRecording context changes
    startRecordingRef.current = startRecording;

    // Step 1 - Replaced stopRecording()
    const stopRecording = async () => {
        if (!recorderRef.current) return;

        await recorderRef.current.stop();
        recorderRef.current = null;

        sendUtteranceEnd();

        setRecording(false);
        setVoiceState("thinking");
    };

    // Step 2 - Added microphone toggle
    const toggleRecording = async () => {
        if (recording) {
            await stopRecording();
        } else {
            await startRecording();
        }
    };

    // Step 3 - Auto restart listening after AI finishes
    useEffect(() => {
        const handler = async () => {
            console.log("🎤 AI finished speaking");
            setAiSpeaking(false);
            setVoiceState("idle");

            // Small delay and guard before auto-restarting the mic. Use
            // recorderRef.current to check whether a recorder already exists
            // (prevents rapid start/stop loops), and ensure the backend is
            // still connected.
            await new Promise(r => setTimeout(r, 200));
            if (!recorderRef.current && isConnected() && startRecordingRef.current) {
                await startRecordingRef.current();
            }
        };

        window.addEventListener("ai-finished", handler);

        return () => {
            window.removeEventListener("ai-finished", handler);
        };
    }, []);

    return (
        <div className="flex flex-col items-center gap-6 p-6">
            {/* Enhanced microphone button with pulse and shadow effects */}
            <div className="relative flex items-center justify-center">
                {/* Pulse effect background when idle */}
                {!recording && (
                    <motion.div
                        animate={{ scale: [1, 1.2, 1], opacity: [0.5, 0, 0.5] }}
                        transition={{ duration: 2, repeat: Infinity }}
                        className="absolute w-32 h-32 rounded-full bg-gradient-to-r from-blue-500 to-cyan-500"
                    />
                )}
                
                {/* Pulse effect background when recording */}
                {recording && (
                    <motion.div
                        animate={{ scale: [1, 1.15, 1], opacity: [0.6, 0.2, 0.6] }}
                        transition={{ duration: 1.5, repeat: Infinity }}
                        className="absolute w-32 h-32 rounded-full bg-gradient-to-r from-red-500 to-pink-500"
                    />
                )}

                {/* Main button */}
                <motion.button
                    onClick={toggleRecording}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                    animate={{ 
                        scale: recording ? [1, 1.05, 1] : 1,
                        boxShadow: recording 
                            ? "0 0 30px 10px rgba(239, 68, 68, 0.5), 0 0 60px 20px rgba(239, 68, 68, 0.25)"
                            : "0 0 30px 10px rgba(59, 130, 246, 0.5), 0 0 60px 20px rgba(59, 130, 246, 0.25)"
                    }}
                    transition={{ 
                        duration: 1.5, 
                        repeat: recording ? Infinity : 0,
                        repeatType: "reverse"
                    }}
                    className={`relative z-10 p-8 rounded-full text-white font-bold shadow-2xl transition-all duration-300 ${
                        recording 
                            ? "bg-gradient-to-br from-red-500 to-red-600 hover:from-red-600 hover:to-red-700" 
                            : "bg-gradient-to-br from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700"
                    }`}
                >
                    <Mic className="h-10 w-10" />
                </motion.button>
            </div>

            <div className="text-center">
                <div className="text-lg font-semibold text-white mb-2">
                    {recording ? "🔴 Recording..." : "🎤 Ready to listen"}
                </div>
                <div className="text-sm font-medium text-gray-400">
                    State: <span className="capitalize font-bold text-cyan-400">{voiceState}</span>
                </div>
                <div className="text-xs text-gray-500 mt-1">
                    Deepgram: <span className={dgStatus === "ready" ? "text-green-400" : "text-red-400"}>{dgStatus || "disconnected"}</span>
                </div>
            </div>
        </div>
    );
}
