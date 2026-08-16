
export default class PCMRecorder {

    constructor(onAudio) {

        this.onAudio = onAudio;

        this.audioContext = null;
        this.stream = null;
        this.source = null;
        this.worklet = null;

        this.recording = false;
    }

    async start() {

        if (this.recording) return;

        this.stream = await navigator.mediaDevices.getUserMedia({
            audio: {
                channelCount: 1,
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: true,
            },
        });

        this.audioContext = new AudioContext({
            sampleRate: 16000,
        });

        await this.audioContext.audioWorklet.addModule(
            "/pcm-processor.js"
        );

        this.source = this.audioContext.createMediaStreamSource(
            this.stream
        );

        this.worklet = new AudioWorkletNode(
            this.audioContext,
            "pcm-processor"
        );

        this.worklet.port.onmessage = (event) => {

            if (!this.recording) return;

            const float32 = event.data;

            // Ensure audio is at 16000Hz for the backend Deepgram websocket
            const targetSampleRate = 16000;
            const sourceSampleRate = this.audioContext ? this.audioContext.sampleRate : targetSampleRate;
            let samples = float32;

            if (sourceSampleRate !== targetSampleRate) {
                // Simple linear resampling
                const sampleRateRatio = sourceSampleRate / targetSampleRate;
                const newLength = Math.round(float32.length / sampleRateRatio);
                const resampled = new Float32Array(newLength);
                for (let i = 0; i < newLength; i++) {
                    const srcIndex = i * sampleRateRatio;
                    const srcIndexFloor = Math.floor(srcIndex);
                    const srcIndexCeil = Math.min(float32.length - 1, srcIndexFloor + 1);
                    const weight = srcIndex - srcIndexFloor;
                    resampled[i] = (1 - weight) * float32[srcIndexFloor] + weight * float32[srcIndexCeil];
                }
                samples = resampled;
            }

            const pcm16 = new Int16Array(samples.length);

            for (let i = 0; i < samples.length; i++) {
                let s = Math.max(-1, Math.min(1, samples[i]));
                pcm16[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
            }

            this.onAudio(
                pcm16.buffer
            );

        };

        this.source.connect(this.worklet);

        // Do not connect the worklet to the audio output. Connecting to
        // audioContext.destination causes playback/loopback in some browsers
        // and is unnecessary for capturing PCM data for the websocket.
        // this.worklet.connect(this.audioContext.destination);


        this.recording = true;

        console.log("🎤 PCM Recorder Started");

    }

    async stop() {

        if (!this.recording) return;

        this.recording = false;

        if (this.worklet) {

            this.worklet.disconnect();

            this.worklet = null;

        }

        if (this.source) {

            this.source.disconnect();

            this.source = null;

        }

        if (this.stream) {

            this.stream
                .getTracks()
                .forEach(track => track.stop());

            this.stream = null;

        }

        if (this.audioContext) {

            await this.audioContext.close();

            this.audioContext = null;

        }

        console.log("🛑 PCM Recorder Stopped");

    }

}