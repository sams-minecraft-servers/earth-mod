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
| 6 | The whole planet's elevation usable by the mod (packed tiles and a reader for them) | done (packing finished 2026-10-13, 65,341 tiles; Everest, the Challenger Deep and Baltimore checked on the test server) | pack log ends "finished: everything is packed"; a place outside the Alps generates correctly |
| 7 | Biomes from measured climate (Koeppen-Geiger map, optionally WorldClim) instead of latitude | not started | jungle, desert, taiga and tundra appear where they really are, without straight edges |
| 8 | Real land below sea level stays below it (Dead Sea shore, Death Valley, polders); today it is flattened | not started | the Dead Sea shore is at about y 74 and dry |
| 9 | Noise caves and large ore veins | built 2026-10-15 (commit 253d03d): the game's noise caves and copper/iron veins by depth below the real ground, sealed under water; checked at Genoa and Mont Blanc on the test server; not yet on the live world | they appear, by depth below the real ground, and never open into water |
| 10 | Where players first appear (0,0 is open sea) | to decide | the owner names the place or places |
| 11 | The server runs under the supervisor and wrapper like the others, then replaces the current earth.tj | done 2026-10-13: earth.tj runs this mod under the supervisor; claims, warps and the map page converted | it starts from the control panel; claims, warps and the map page work on the new world |

## Immersion (asked for on 2026-10-13)

| # | Goal | Status | Done when |
|---|------|--------|-----------|
| 12 | Live sky: the time of day follows real longitude, the weather is the real weather where the player stands | not started | noon in Paris while it is night in Tokyo; rain in game where it rains today |
| 13 | Regional seasons with an unmodified game: winter snow and bare colours, opposite in the two hemispheres, wet and dry seasons in the tropics | not started | the Alps are snowy in January while Australia is in summer; nothing is lost from the saved world when the season turns |
| 14 | A sky page on the earth.tj website: the live time, weather and season across the map | not started | the page shows the same sky a player sees in game at that place |
| 15 | Named places: a notice on entering a town or country, latitude and longitude on screen, and a command to find any real place | built 2026-10-15 in the wrapper (not yet deployed): a title on crossing into a country or town, a location bar with town, country, latitude and longitude (!coords), !find for any place; towns from GeoNames, borders from Natural Earth, all on this machine | walking into Chamonix says so; the command finds Kyoto |
| 16 | An economy driven by geography: ores, crops and animals where they really are, so trade between regions matters | not started | a written table of what is found where, and the world follows it |
| 17 | Real city footprints: real streets and building outlines (OpenStreetMap) for players to claim and build up; gives the villagers homes and work. Decided 2026-10-13: at the true scale of the map (a house is a block or two), not enlarged | trial done on the test server for central Genoa (2026-10-14): streets, buildings by outline and height, bridges. Not started: packing the rest of the planet, walls and roofs by region, a find-my-address command, homes and jobs for villagers, keeping buildings out from under monuments | Genoa's streets are recognisable from above; villagers have beds and jobs |
| 18 | Regional radio, only on earth.tj: one station per country, heard in that country and, with radio static that grows with distance, for some way beyond it (the static is a separate looping sound whose loudness the wrapper sets from the distance to the country). Stations live in extra resource packs sent by the separate mod `/home/ubuntu/server-packs-mod` (`serverpack send` / `serverpack remove`); the wrapper keeps deciding what plays. Adding a pack shows the loading screen, which cannot be avoided, so packs are sent on joining, on a warp, or when the player tunes to a station they do not have yet. Decided 2026-10-13: the loading screen comes when a player chooses a station they do not have yet; players collect stations by exploring (first setting foot in a country adds its station to their dial for good). Stations are real broadcasters, sampled and refreshed every day or few days; the owner asks each for permission before the server goes live (list: `radio/stations.json`, emailed 2026-10-13), and a country's pack is only published once its station says yes | built 2026-10-15, not yet deployed: wrapper !tune / !dial (stations collected on entering a country, sent by expiring links, static by distance from the border); daily refresh timer installed (permitted stations only). Waiting on: station permissions (0 of 241), installing the server-packs mod on earth.tj, a real client loading a pack. Only "testers" in config/earth_radio.json can hear stations without permission | standing in France the French station is clear, across the border it crackles, far away it is gone; a station appears on a player's dial the first time they enter its country and stays; a real client loads a second pack and hears it |
| 19 | Vegetation particular to a region, starting with giant sequoias in California; more to be listed | not started | each listed plant grows only in its real range |
| 20 | Underwater landmarks: the Edmund Fitzgerald (Lake Superior) and the Titanic (North Atlantic) at their real positions and depths; more to be listed. Asked 2026-10-14: many wrecks, several times life size so they can be swum through | 47 wrecks built and rehearsed on the test server (Titanic at y -597, Edmund Fitzgerald in a dug basin); not yet placed on the live world | each wreck stands on the real lake or sea bed at its coordinates |
| 21 | A hidden Atlantis: a sunken city nobody is told about | built 2026-10-15: tools/landmarks/atlantis.js picks a random spot on the Atlantic floor, kept in a secret folder; rehearsed on the test server; not yet placed on the live world | it exists; its position is written nowhere a player can read |
| 22 | The world does not feel empty: a live map of players and land claims on the website (asked for 2026-10-13, with claims kept); starting players in a few hub cities is still only a suggestion | done: the home page and the map page (earth.tj/map) show who is online, the claims as their real squares, and the landmarks; checked on the live API 2026-10-15 (4 players in Baltimore) | the map page shows claims and who is where on the new world |
| 23 | Animals where they really live (asked 2026-10-15): pandas, polar bears, camels, llamas, parrots, ocelots, armadillos, wolves, foxes, goats, wild horses, donkeys, turtles, sea fish by water temperature, nautiluses, axolotls in Mexico City | built 2026-10-15 (Fauna.java): seen on the test server in Qinling (pandas), the Sahara (camels), Svalbard (polar bears), the Altiplano (llamas, armadillos); not yet on the live world | each listed animal appears only in its real range |

## Fixes asked for on 2026-10-14

- The sea was not level (blobs of raised water in harbours) and every shore stood two blocks over
  the water. Fixed in `Terrain` and checked on the test server at Genoa: of 62,318 water columns,
  97 are not at sea level (an inland pond), and the land at the water's edge is level with it.
  Chunks made before the fix keep the old shape.
- Monuments (about 200, in the wrapper's `tools/landmarks`) are not yet built in this world; the
  Tower of Pisa was placed on the test server with the same tools.

Plans for the goals not started are in PLANS.md (2026-10-15).

## Checking a goal off

A goal is finished only when (a) it meets its "done when" on the test server, (b) it is committed,
and (c) somebody has seen it in the game with an ordinary client. Mark (c) separately: write
"seen in game, <date>" in the status.
