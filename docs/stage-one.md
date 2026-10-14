# Stage One: The Gauntlet

Budget: **$500 cash plus the laptop you already own.** Nothing else gets spent.

Goal: one working, wearable piece you can film from day one. It's a right-hand gauntlet with a glowing palm repulsor that reacts to your hand's motion, plus ADAM as a voice assistant on the laptop that can trigger it.

Prices are typical US retail estimates from late 2026 (Amazon, AliExpress, Adafruit). Check them before you buy.

## What the laptop covers (free)

| Job | Free software |
| --- | --- |
| ADAM voice assistant | Python, Vosk or Whisper for offline speech recognition |
| Gauntlet firmware | Arduino IDE or PlatformIO |
| Designing parts | FreeCAD, or Fusion 360's free personal licence |
| Slicing prints | Bambu Studio, PrusaSlicer or Cura |
| Editing build videos | DaVinci Resolve or CapCut |

## Parts list

| Part | Why | Est. cost |
| --- | --- | --- |
| ESP32 dev board (x2, one spare) | The gauntlet's brain, with Wi-Fi and Bluetooth to talk to the laptop | $15 |
| WS2812B 16-LED ring | Palm repulsor light | $8 |
| MPU-6050 motion sensor | Detects a palm-out "fire" gesture | $5 |
| Small vibration motor + mini speaker | Feedback when it fires | $8 |
| 18650 battery, holder, TP4056 charge board | Wireless power | $20 |
| Electronics starter kit (breadboard, jumpers, resistors, switches) | Prototyping | $20 |
| Soldering iron kit with solder and wick | Making it permanent | $30 |
| Entry 3D printer (Bambu Lab A1 mini or similar) | Prints the armor shell and the parts you'll sell | $200–250 |
| 2 rolls of PLA | Shell material | $35 |
| Filler primer, sandpaper, metallic paint, clear coat | A red and gold finish that reads as metal | $40 |
| **Total** | | **≈ $380–430** |

The printer is the core purchase. It makes the shell, and it lets you sell printed parts and test the STL designs you'll list. If money gets tight, a makerspace or library printer is the fallback.

The printed parts also become molds for fiberglass or carbon fiber shells in stage two, and the designs later become cut aluminum or steel plates.

## Build order

1. **Week 1:** Get ADAM listening on the laptop. Say "ADAM, repulsor" and it prints a response.
2. **Week 2:** Wire the ESP32, LED ring and motion sensor on a breadboard. Raise your palm and the light fires.
3. **Week 3:** Connect them. The voice command or the gesture fires the repulsor over Wi-Fi.
4. **Week 4:** Print, sand and paint the shell, then mount the electronics.

Film every step. Week 4's reveal is your first real video.

## What comes after

- Publish the gauntlet STL for sale on Cults3D or Etsy.
- Put the leftover money toward the helmet, which is stage two.
- Keep a running total of money spent and earned in `docs/ledger.md`.
