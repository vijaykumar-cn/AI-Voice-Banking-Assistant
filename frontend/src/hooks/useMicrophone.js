import { useRef, useState } from "react";
import { sendAudio } from "../services/websocket";

export default function useMicrophone() {

    const recorderRef = useRef(null);
    const streamRef = useRef(null);

    const [recording, setRecording] = useState(false);

    const startRecording = async () => {

        const stream = await navigator.mediaDevices.getUserMedia({
            audio: true,
        });

        streamRef.current = stream;

        const recorder = new MediaRecorder(stream);

        recorderRef.current = recorder;

       recorder.ondataavailable = async (event) => {

    console.log("Audio Type:", event.data.type);
    console.log("Audio Size:", event.data.size);

    if (event.data.size > 0) {

        const buffer = await event.data.arrayBuffer();

        console.log("Buffer Size:", buffer.byteLength);

        sendAudio(buffer);

    }


        };

        recorder.start(250);

        setRecording(true);

        console.log("Recording...");

    };

    const stopRecording = () => {

        recorderRef.current.stop();

        streamRef.current.getTracks().forEach(track => track.stop());

        setRecording(false);

        console.log("Stopped");

    };

    return {
        recording,
        startRecording,
        stopRecording
    };
}