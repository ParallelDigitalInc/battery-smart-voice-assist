# Battery Smart — Voice Assistant V2 prototype

Interactive HTML prototype of the voice assistant for the overdue-plan state: the
plan card on Home, the सुनिए sheet with seven narrated steps, the breakdown card
growing in sync with the voice, and the final pay / return state.

## Files
| File | What it is |
|---|---|
| `battery-smart-voice-v2-audio.html` | **Single file, clips embedded.** Open in Chrome. This is the one to share. |
| `index.html` | Same prototype, loads clips from `audio/`. Use this when iterating. |
| `audio/step-01…08.mp3` | Ritu (Sarvam) narration, one clip per line. `step-04` is unused (the ₹300 line was cut). |
| `generate_audio.py` | Regenerates the clips from the `tts:` lines in `index.html` via Sarvam TTS. |
| `assets/` | Client SVGs: ∞ plan glyph, calendar and wallet illustrations. |
| `docs-identity-round2.html` | Identity exploration board (reference, not part of the prototype). |

## Run
Open `battery-smart-voice-v2-audio.html` in Chrome. Tap the speaker on the plan card.

Controls in the sheet: **sound** (mute keeps captions running), **waveform**
(tap to pause), **pause/play**, then **back · dots · forward**. A manual pause is
sticky across back/forward. Keyboard: space, ← →, M, Esc.

Two variants, switched with the **CTAs** button in the prototype toolbar:

- **CTAs: at end** (default) - Pay / Return Battery and Contact Support appear
  once the narration has finished.
- **CTAs: always** - client-requested variant (19 Sep). A Support button sits in
  the sheet header throughout, and Pay / Return Battery are in the sheet from the
  first line. Link directly with `?cta=early`, e.g.
  `index.html?cta=early`.

## Changing the numbers
Everything the voice says lives in the `CONFIG` object at the top of the script.
Change one value and the Home card, the sheet card, the captions and the TTS text
all follow. The countdown is one live clock shared by every surface.

## Regenerating audio
```
export SARVAM_API_KEY=sk_...
python3 generate_audio.py --speaker ritu --model bulbul:v3
```
Then rebuild the single file (the embedded clips are the ones in `audio/`):
```
python3 - <<'PY'
import base64,json
s=open('index.html',encoding='utf-8').read()
u=['data:audio/mpeg;base64,'+base64.b64encode(open(f'audio/step-0{i}.mp3','rb').read()).decode() for i in range(1,9)]
open('battery-smart-voice-v2-audio.html','w',encoding='utf-8').write(s.replace('<script>\n/* ═','<script>window.EMBEDDED_AUDIO='+json.dumps(u)+';</script>\n<script>\n/* ═',1))
PY
```

## Design sources
- Voice flow: Figma `J4zIIUsnOHgygwt6CvVedA`, section V2 (1346-13058)
- Identity: option 4-1 (1478-17844), gradient disc + speaker, Figma motion loop
- Home card: Swap & BaaS int `wRInRz5VZ4p0txXzDAC4Qm`, node 2102-60333
- Tokens: Battery Smart design system (M3, light only)

## Known deviations from Figma
- Home card numbers follow `CONFIG` (4 days / +₹50 / ₹3,399) so Home and the sheet agree, rather than the frame's placeholders.
- The `+₹100 / 02m 04s` strip in the frames is replaced by one consistent countdown and `+₹50`.
- Avatar photo is a placeholder.
