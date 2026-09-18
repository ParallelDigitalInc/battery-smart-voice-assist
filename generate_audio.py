#!/usr/bin/env python3
"""
Generate the 8 narration clips with Sarvam AI TTS and drop them into ./audio.
The prototype picks them up automatically (audio/step-01.wav … step-08.wav).

Usage:
    export SARVAM_API_KEY=sk_...
    python3 generate_audio.py                # defaults: model bulbul:v3, speaker ritu
    python3 generate_audio.py --speaker ritu --model bulbul:v3 --pace 0.95

The Hindi lines are read straight out of index.html (the `tts:` field of each
step), so the audio can never drift from the captions. Edit the copy in one place.
"""
import argparse, base64, json, os, re, sys, time, urllib.request, urllib.error

ap = argparse.ArgumentParser()
ap.add_argument("--speaker", default="ritu")
ap.add_argument("--model", default="bulbul:v3")
ap.add_argument("--pace", type=float, default=0.95)
ap.add_argument("--lang", default="hi-IN")
ap.add_argument("--rate", type=int, default=22050, help="speech_sample_rate")
ap.add_argument("--html", default=os.path.join(os.path.dirname(__file__), "index.html"))
ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "audio"))
args = ap.parse_args()

key = os.environ.get("SARVAM_API_KEY")
if not key:
    sys.exit("Set SARVAM_API_KEY first (dashboard.sarvam.ai → API keys).")

html = open(args.html, encoding="utf-8").read()
lines = re.findall(r"tts:\s*`([^`]+)`", html)
if len(lines) != 8:
    sys.exit(f"Expected 8 tts lines in index.html, found {len(lines)}.")

os.makedirs(args.out, exist_ok=True)
url = "https://api.sarvam.ai/text-to-speech"

def call(text):
    body = {
        "text": text,                       # current API shape
        "inputs": [text],                   # older shape, harmless if ignored
        "target_language_code": args.lang,
        "speaker": args.speaker,
        "model": args.model,
        "pace": args.pace,
        "speech_sample_rate": args.rate,
        "enable_preprocessing": True,
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
        headers={"api-subscription-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))

for i, text in enumerate(lines, 1):
    path = os.path.join(args.out, f"step-{i:02d}.wav")
    print(f"[{i}/8] {text}")
    try:
        res = call(text)
    except urllib.error.HTTPError as e:
        sys.exit(f"  Sarvam returned {e.code}: {e.read().decode('utf-8', 'ignore')[:400]}\n"
                 f"  If the error names the speaker or model, list what your account offers and pass --speaker/--model.")
    b64 = res["audios"][0]
    open(path, "wb").write(base64.b64decode(b64))
    print(f"      → {path}")
    time.sleep(0.3)

print("\nDone. Open index.html and tap the speaker on the plan card.")
