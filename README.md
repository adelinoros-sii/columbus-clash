# Columbus Clash

Retro pixel fighting game set in the Columbus tavern on Halloween night. Alen, Serj, Ade and Odi fight in story mode, vs CPU, local 2 player, or online.

- Controls: WASD move, J/I low/high punch, K/O low/high kick, L block, U special, Space super. Local P2 uses a gamepad or arrows + numpad.
- Phones: touch controls appear automatically (slide on the d-pad for motions). Landscape puts the controls over the screen. FULL goes fullscreen on Android; on iPhone use Add to Home Screen.
- Elements: every fighter picks one of 8 elements (lightning, fire, earth, shadow, wind, water, ice, light) on the select screen with W/S. The element sets special 1 (projectile), the super and two power kombos: HP, LP, HP, HK and LK, HP, LK, HP. Each hero starts on a signature element: Alen lightning, Serj fire, Ade earth, Odi shadow.
- Fight feel: super cut-ins, camera punch-ins, counter hits, combo praise, LAST STAND (under 25% health your meter fills once and that super becomes an ULTRA), announcer voice (browser speech) and a chiptune soundtrack with a final-round theme. A slow-motion replay plays after the deciding KO (any key skips).
- Taunt with T (P2: Numpad 7) and quick chat with keys 1-6. Results offer FIGHT BACK! for an instant rematch.
- Solo modes: SURVIVAL (one-round fights in a row against random CPU rivals that get harder, 30% heal between fights, best run saved) and TRAINING (dummy can stand, crouch, block, jump or fight as a CPU; no timer, no KO, infinite super, damage and combo readout).
- Pause (Esc or PAUSE on phones) has a full MOVE LIST for your fighter and an EFFECTS option; EFFECTS: REDUCED tones down screen shake, flashes and camera zoom.
- Install: the Vercel site is an installable app (Add to Home Screen, or INSTALL APP on the title screen in Chrome). After the first visit it starts offline; online matches still need a connection.
- Party modes: Tag Team 2v2 (T tags), Winner Stays On (2-8 named players) and a 3-way Free For All.
- Unlockables: 7 costumes (U on the select screen) and 4 stages (pick on the title screen), unlocked by playing. EXTRAS shows your record, rivals and unlocks. Stats are saved in the browser.
- Online: name yourself in the lobby to track rivalries. CREATE ROOM + INVITE shares or copies the link in one tap. Friends can watch with the watch link (or WATCH + code); spectators stay in sync from the host's inputs.
- Online matches use Supabase Realtime (project `columbus-clash`) to set up rooms, then a direct WebRTC connection between the two browsers when it's available. The game runs in input-delay lockstep and resyncs automatically if the two sides drift apart.
- Source is `src/columbus-clash.html`; `index.html` + `assets/` are built from it.
- Deploy: import this repo in Vercel (framework "Other", no build command). Every push to `main` redeploys.
- Edit `src/columbus-clash.html`, then run `python3 tools/build.py src/columbus-clash.html .` before pushing. It moves the inlined images into `assets/` (cached forever) so `index.html` stays small and the game loads fast. It also writes `manifest.webmanifest` and `sw.js` (the offline cache list); the icons live in `icons/`.

## Credits

Power and hit effects are rendered with [pixelfx](https://github.com/patch-gg/pixelfx) by Patch and Hugo Duprez (MIT License). Story enemy sprites: "Bad Company" universal prototype by Stonewall (CC0).

Play it at https://columbus-clash.vercel.app
