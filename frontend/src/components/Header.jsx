import { Building2 } from "lucide-react";

export default function Header() {
    return (
        <header className="bg-slate-900 border-b border-slate-700 h-16 flex items-center justify-between px-8">

            <div className="flex items-center gap-3">

                <Building2
                    size={34}
                    className="text-blue-500"
                />

                <div>

                    <h1 className="text-2xl font-bold">
                        AI Bank Assistant
                    </h1>

                    <p className="text-sm text-gray-400">
                        Voice Banking Assistant
                    </p>

                </div>

            </div>

            <div className="flex items-center gap-2">

                <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse"/>

                <span>
                    Connected
                </span>

            </div>

        </header>
    );
}