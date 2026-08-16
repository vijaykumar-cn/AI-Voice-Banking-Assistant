let socket = null;
let messageHandler = null;
let connectAttempts = 0;
let shouldReconnect = true;

const MAX_CONNECT_ATTEMPTS = 3;
const CONNECT_RETRY_DELAY_MS = 500;

function _retryConnect() {
    if (connectAttempts >= MAX_CONNECT_ATTEMPTS) {
        console.warn("WebSocket: max retry attempts reached");
        return;
    }

    connectAttempts += 1;
    console.log(`WebSocket: retrying connection (${connectAttempts}/${MAX_CONNECT_ATTEMPTS})`);
    setTimeout(() => {
        if (socket && (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING)) {
            return;
        }

        connect();
    }, CONNECT_RETRY_DELAY_MS);
}

function _onMessage(event) {
    try {
        // Binary frames are handled elsewhere (sendAudio)
        if (typeof event.data === "string") {
            const response = JSON.parse(event.data);
            console.log("📩 Backend:", response);
            if (messageHandler) messageHandler(response);

            if (response.audio) {
                console.log("Playing audio URL:", response.audio);
                const audio = new Audio(response.audio);
                // Helpful for debugging autoplay/CORS/decoding issues
                audio.crossOrigin = "anonymous";
                audio.onplay = () => console.log("🔊 AI Speaking...");
                audio.onended = () => {
                    console.log("✅ AI Finished Speaking");
                    window.dispatchEvent(new CustomEvent("ai-finished"));
                };
                audio.onerror = (e) => console.error("Audio Error", e);
                audio.play().catch((err) => {
                    console.error("Failed to play audio:", err, "— ensure user gesture/autoplay policy, check /audio/<file> network request and that the file exists and is served with correct MIME type.");
                });
            }
        } else {
            // Received binary data (unlikely for this app from server)
            console.log("Received binary message from server");
        }
    } catch (err) {
        console.log("Failed to parse websocket message", err, event.data);
    }
}

function _onOpen() {
    console.log("🔌 WebSocket connected");
    connectAttempts = 0;
}

function _onClose(event) {
    console.log("🔌 WebSocket disconnected", {
        code: event?.code,
        reason: event?.reason,
        wasClean: event?.wasClean,
        readyState: socket?.readyState,
        url: socket?.url,
        shouldReconnect,
    });
    socket = null;
    if (shouldReconnect) {
        _retryConnect();
    }
}

function _onError(e) {
    console.error("WebSocket error", e, {
        readyState: socket?.readyState,
        url: socket?.url,
    });
}

function _buildUrl() {
    const protocol = location.protocol === "https:" ? "wss" : "ws";
    // Use IPv4 localhost when the app is running locally to avoid IPv6 resolution issues.
    const localHostnames = ["localhost", "::1", "0.0.0.0"];
    const host = localHostnames.includes(location.hostname)
        ? "127.0.0.1"
        : location.hostname;
    const url = `${protocol}://${host}:8001/voice`;
    console.debug("WebSocket URL:", url);
    return url;
}

export function connect(onMessage) {
    if (onMessage) {
        messageHandler = onMessage;
    }

    shouldReconnect = true;

    if (socket) {
        if (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING) {
            return;
        }

        socket = null;
    }

    const url = _buildUrl();
    console.log("WebSocket: opening", url);
    socket = new WebSocket(url);
    socket.binaryType = "arraybuffer";
    socket.onopen = _onOpen;
    socket.onmessage = _onMessage;
    socket.onclose = _onClose;
    socket.onerror = _onError;
}

export function disconnect() {
    shouldReconnect = false;
    if (!socket) return;
    try {
        socket.close();
    } catch (e) {
        console.warn("Error closing websocket", e);
    }
    socket = null;
    connectAttempts = 0;
}

export function isConnected() {
    return !!(socket && socket.readyState === WebSocket.OPEN);
}

export function sendAudio(arrayBuffer) {
    if (!socket || socket.readyState !== WebSocket.OPEN) return;
    try {
        socket.send(arrayBuffer);
    } catch (e) {
        console.error("Failed to send audio", e);
    }
}

export function sendUtteranceEnd() {
    if (!socket || socket.readyState !== WebSocket.OPEN) return;
    try {
        socket.send(JSON.stringify({ type: "utterance_end" }));
    } catch (e) {
        console.error("Failed to send utterance_end", e);
    }
}