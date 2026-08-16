import { User, ShieldCheck } from "lucide-react";
import { useVoice } from "../context/VoiceContext";

export default function CustomerCard() {

    const { customer } = useVoice();

    return (
        <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">

            <div className="flex items-center gap-3 mb-6">
                <User
                    className="text-blue-500"
                    size={28}
                />

                <h2 className="text-2xl font-bold">
                    Customer
                </h2>
            </div>

            {customer ? (

                <div className="space-y-5">

                    <div>
                        <p className="text-sm text-slate-400">
                            Name
                        </p>

                        <p className="text-lg font-semibold">
                            {customer.name}
                        </p>
                    </div>

                    <div>
                        <p className="text-sm text-slate-400">
                            Customer ID
                        </p>

                        <p className="text-lg font-semibold">
                            {customer.customer_id}
                        </p>
                    </div>

                    <div className="flex items-center gap-2 text-green-400">

                        <ShieldCheck size={22} />

                        Verified Customer

                    </div>

                </div>

            ) : (

                <div className="text-slate-400">
                    No customer verified yet.
                </div>

            )}

        </div>
    );
}