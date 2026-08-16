import CustomerCard from "./CustomerCard";
import VoicePanel from "./VoicePanel";
import ChatWindow from "./ChatWindow";
import StatusCards from "./StatusCards";

export default function Dashboard() {
    return (
        <div className="min-h-[calc(100vh-64px)] bg-slate-950 p-6">

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">

                {/* Left Panel */}
                <div className="lg:col-span-3 space-y-6">
                    <CustomerCard />
                    <StatusCards />
                </div>

                {/* Center Panel */}
                <div className="lg:col-span-5">
                    <VoicePanel />
                </div>

                {/* Right Panel */}
                <div className="lg:col-span-4">
                    <ChatWindow />
                </div>

            </div>

        </div>
    );
}