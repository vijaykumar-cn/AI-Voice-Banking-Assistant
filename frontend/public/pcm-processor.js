class PCMProcessor extends AudioWorkletProcessor {

    process(inputs) {

        const input = inputs[0];

        if (!input || input.length === 0) {
            return true;
        }

        const channel = input[0];

        // Send Float32 PCM samples to main thread
        this.port.postMessage(channel);

        return true;
    }
}

registerProcessor("pcm-processor", PCMProcessor);   