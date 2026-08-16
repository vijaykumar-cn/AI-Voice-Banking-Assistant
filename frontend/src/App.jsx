import Home from "./pages/Home";
import { VoiceProvider } from "./context/VoiceContext";

export default function App() {

    return (

        <VoiceProvider>

            <Home />

        </VoiceProvider>

    );

}