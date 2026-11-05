# Columbus Clash

Retro pixel fighting game set in the Columbus tavern on Halloween night. Alen, Serj, Ade and Odi fight in story mode, vs CPU, local 2 player, or online.

- Controls: WASD move, J/I low/high punch, K/O low/high kick, L block, U special, Space super. Local P2 uses a gamepad or arrows + numpad.
- Phones: touch controls appear automatically (slide on the d-pad for motions). Landscape puts the controls over the screen. FULL goes fullscreen on Android; on iPhone use Add to Home Screen.
- Elements: every fighter picks one of 8 elements (lightning, fire, earth, shadow, wind, water, ice, light) on the select screen with W/S. The element sets special 1 (projectile), the super and two power kombos: HP, LP, HP, HK and LK, HP, LK, HP. Each hero starts on a signature element: Alen lightning, Serj fire, Ade earth, Odi shadow.
- Everything is in one file: `index.html`. There's no build step.
- Online matches use Supabase Realtime (project `columbus-clash`) to set up rooms, then a direct WebRTC connection between the two browsers when it's available. The game runs in input-delay lockstep and resyncs automatically if the two sides drift apart.
- Deploy: import this repo in Vercel (framework "Other", no build command). Every push to `main` redeploys.
- Edit `src/columbus-clash.html`, then run `python3 tools/build.py src/columbus-clash.html .` before pushing. It moves the inlined images into `assets/` (cached forever) so `index.html` stays small and the game loads fast.

## Credits

Power and hit effects are rendered with [pixelfx](https://github.com/patch-gg/pixelfx) by Patch and Hugo Duprez (MIT License). Story enemy sprites: "Bad Company" universal prototype by Stonewall (CC0).

Play it at https://columbus-clash.vercel.app
