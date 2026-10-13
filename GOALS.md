# Goals for the new earth.tj

Everything the owner has asked for on this server, with what "done" means for each, so it can be
gone through later and checked. Status is one of: **done** (built and checked on the test server),
**running**, **not started**, **to decide** (waiting on the owner). Nothing here has been walked
through by a real player yet; that is a separate check for every item.

Last updated 2026-10-13.

## The world itself

| # | Goal | Status | Done when |
|---|------|--------|-----------|
| 1 | The real Earth at 1:5, generated as chunks are needed, using the full height (Y -2032 to 2031, 5 m per block) | done | Mont Blanc's summit is at y 1120; Everest and the Challenger Deep fit |
| 2 | Real land cover, lakes and rivers at their own level | done | Genoa harbour and Lake Geneva look right on the test server |
| 3 | Ores, caves, mineshafts, strongholds and trial chambers at their usual depth below the real ground; no cave under water | done | `tools/underground.py` shows vanilla depths |
| 4 | Ocean monuments on the real sea bed; strongholds spread over the map; no vanilla villages; villagers in built-up land | done | checked south of Genoa and at Genoa |
| 5 | The whole planet's data on this machine | done | download log ends "finished: everything is here" (2026-10-13) |
| 6 | The whole planet's elevation usable by the mod (packed tiles and a reader for them) | running | pack log ends "finished: everything is packed"; a place outside the Alps generates correctly |
| 7 | Biomes from measured climate (Koeppen-Geiger map, optionally WorldClim) instead of latitude | not started | jungle, desert, taiga and tundra appear where they really are, without straight edges |
| 8 | Real land below sea level stays below it (Dead Sea shore, Death Valley, polders); today it is flattened | not started | the Dead Sea shore is at about y 74 and dry |
| 9 | Noise caves and large ore veins | not started | they appear, by depth below the real ground, and never open into water |
| 10 | Where players first appear (0,0 is open sea) | to decide | the owner names the place or places |
| 11 | The server runs under the supervisor and wrapper like the others, then replaces the current earth.tj | not started | it starts from the control panel; claims, warps and the map page work on the new world |

## Immersion (asked for on 2026-10-13)

| # | Goal | Status | Done when |
|---|------|--------|-----------|
| 12 | Live sky: the time of day follows real longitude, the weather is the real weather where the player stands | not started | noon in Paris while it is night in Tokyo; rain in game where it rains today |
| 13 | Regional seasons with an unmodified game: winter snow and bare colours, opposite in the two hemispheres, wet and dry seasons in the tropics | not started | the Alps are snowy in January while Australia is in summer; nothing is lost from the saved world when the season turns |
| 14 | A sky page on the earth.tj website: the live time, weather and season across the map | not started | the page shows the same sky a player sees in game at that place |
| 15 | Named places: a notice on entering a town or country, latitude and longitude on screen, and a command to find any real place | not started | walking into Chamonix says so; the command finds Kyoto |
| 16 | An economy driven by geography: ores, crops and animals where they really are, so trade between regions matters | not started | a written table of what is found where, and the world follows it |
| 17 | Real city footprints: real streets and building outlines (OpenStreetMap) for players to claim and build up; gives the villagers homes and work | not started | Genoa's streets are recognisable from above; villagers have beds and jobs |
| 18 | Regional radio, only on earth.tj: the stations a player hears depend on where they are | not started | crossing into another region changes the station list |
| 19 | Vegetation particular to a region, starting with giant sequoias in California; more to be listed | not started | each listed plant grows only in its real range |
| 20 | Underwater landmarks: the Edmund Fitzgerald (Lake Superior) and the Titanic (North Atlantic) at their real positions and depths; more to be listed | not started | each wreck stands on the real lake or sea bed at its coordinates |
| 21 | A hidden Atlantis: a sunken city nobody is told about | not started | it exists; its position is written nowhere a player can read |
| 22 | The world does not feel empty: players start in a few hub cities, and the web map shows who is where | to decide | suggested by Claude, not yet asked for by the owner |

## Checking a goal off

A goal is finished only when (a) it meets its "done when" on the test server, (b) it is committed,
and (c) somebody has seen it in the game with an ordinary client. Mark (c) separately: write
"seen in game, <date>" in the status.
