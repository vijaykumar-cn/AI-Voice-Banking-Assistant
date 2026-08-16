import Header from "../components/Header";
import Dashboard from "../components/Dashboard";
import { useVoice } from "../context/VoiceContext";
import { useEffect } from "react";


export default function Home() {

    const {

        setMessages,

        setDgStatus,

        setCustomer,

    } = useVoice();

    

        

    return (

        <div className="min-h-screen bg-slate-950">

            <Header />

            <Dashboard />

        </div>

    );

}