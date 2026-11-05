# Columbus Clash

Retro pixel fighting game set in the Columbus tavern on Halloween night. Alen, Serj, Ade and Odi fight in story mode, vs CPU, local 2 player, or online.

- Everything is in one file: `index.html`. There's no build step.
- Online matches use Supabase Realtime (project `columbus-clash`) to set up rooms, then a direct WebRTC connection between the two browsers when it's available. The game runs in input-delay lockstep and resyncs automatically if the two sides drift apart.
- Deploy: import this repo in Vercel (framework "Other", no build command). Every push to `main` redeploys.

Play it at https://columbus-clash.vercel.app
