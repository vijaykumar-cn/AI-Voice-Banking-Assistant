import useMicrophone from "../hooks/useMicrophone";

export default function MicButton() {
    const {
        recording,
        startRecording,
        stopRecording,
    } = useMicrophone();

    return (
        <div style={{ marginTop: 20 }}>

            {!recording ? (
                <button onClick={startRecording}>
                    🎤 Start Talking
                </button>
            ) : (
                <button onClick={stopRecording}>
                    ⏹ Stop
                </button>
            )}

        </div>
    );
}