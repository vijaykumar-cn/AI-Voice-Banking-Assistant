from kokoro import KPipeline
import soundfile as sf

pipeline = KPipeline(lang_code="a")

text = "Hello Vijay. Welcome to your AI banking assistant."

generator = pipeline(
    text,
    voice="af_heart",
)

for i, (gs, ps, audio) in enumerate(generator):
    sf.write(f"output_{i}.wav", audio, 24000)

print("✅ Audio generated successfully!")