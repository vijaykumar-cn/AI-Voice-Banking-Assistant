import { createContext, useContext, useState } from "react";

const VoiceContext = createContext();

export function VoiceProvider({ children }) {

    const [messages, setMessages] = useState([]);

    const [customer, setCustomer] = useState(null);

    const [recording, setRecording] = useState(false);

    const [dgStatus, setDgStatus] = useState("disconnected");

    const [aiSpeaking, setAiSpeaking] = useState(false);

    // idle | listening | thinking | speaking
    const [voiceState, setVoiceState] = useState("idle");

    const value = {

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

    };

    return (
        <VoiceContext.Provider value={value}>
            {children}
        </VoiceContext.Provider>
    );
}

export function useVoice() {
    return useContext(VoiceContext);
}