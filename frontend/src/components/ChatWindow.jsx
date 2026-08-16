import { useVoice } from "../context/VoiceContext";

export default function ChatWindow() {
    const { messages } = useVoice();

    return (
        <div className="flex h-[680px] flex-col overflow-hidden rounded-[24px] border border-slate-700/70 bg-slate-900/90 shadow-[0_20px_60px_-20px_rgba(2,6,23,0.85)] sm:h-[740px]">
            <div className="border-b border-slate-700/80 bg-gradient-to-r from-slate-800 to-slate-900 px-5 py-4">
                <div className="flex items-center justify-between gap-3">
                    <div>
                        <p className="text-[10px] font-semibold uppercase tracking-[0.3em] text-cyan-400">
                            Live Conversation
                        </p>
                        <h2 className="text-xl font-bold text-white">Conversation</h2>
                    </div>
                    <div className="rounded-full border border-cyan-500/40 bg-cyan-500/10 px-3 py-1 text-xs font-semibold text-cyan-300">
                        {messages.length} messages
                    </div>
                </div>
            </div>

            <div className="flex-1 overflow-y-auto p-5 space-y-4">
                {messages.length === 0 ? (
                    <div className="flex h-full items-center justify-center rounded-2xl border border-dashed border-slate-700/80 bg-slate-800/40 p-6 text-center text-sm text-slate-400">
                        Start speaking to see the conversation flow here.
                    </div>
                ) : (
                    messages.map((msg, i) => (
                        <div
                            key={i}
                            className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-sm ${
                                msg.sender === "AI"
                                    ? "bg-slate-800/90 text-slate-100"
                                    : "ml-auto bg-gradient-to-r from-blue-500 to-cyan-500 text-white"
                            }`}
                        >
                            <div className="mb-1 text-[10px] font-semibold uppercase tracking-[0.25em] opacity-70">
                                {msg.sender === "AI" ? "Bank Assistant" : "You"}
                            </div>
                            <div>{msg.text}</div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}