import {
    Database,
    BrainCircuit,
    Mic,
    Server
} from "lucide-react";

const items = [
    {
        title: "Deepgram",
        icon: Mic,
    },
    {
        title: "Azure",
        icon: BrainCircuit,
    },
    {
        title: "PostgreSQL",
        icon: Database,
    },
    {
        title: "LangGraph",
        icon: Server,
    },
];

export default function StatusCards() {

    return (

        <div className="bg-slate-900 rounded-xl p-6">

            <h2 className="text-xl font-bold mb-5">

                Services

            </h2>

            <div className="space-y-4">

                {items.map((item) => {

                    const Icon = item.icon;

                    return (

                        <div
                            key={item.title}
                            className="flex items-center justify-between"
                        >

                            <div className="flex items-center gap-3">

                                <Icon size={18}/>

                                {item.title}

                            </div>

                            <div className="flex items-center gap-2">

                                <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse"/>

                                Ready

                            </div>

                        </div>

                    );

                })}

            </div>

        </div>

    );

}