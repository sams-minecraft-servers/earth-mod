# Plans for the goals not yet built

Written 2026-10-15 at the owner's request, in the order asked: climate biomes, land below sea
level, then the rest of the goals in GOALS.md that are not started. Each section says what it
would take, what data it needs, what could go wrong, and how it would be checked. Nothing here is
built yet. Sizes and times are estimates.

A rule for all of them: what the mod changes only affects chunks generated after it is deployed.
Land players have already seen stays as it is, so there will be a visible seam at the edge of
explored land unless those chunks are regenerated (which deletes anything built there).

---

## 1. Biomes from measured climate (goal 7)

**Now:** biomes come from land cover (forest, grass, bare...) plus height and latitude, so a
forest at 10°N is jungle and the same forest at 30°N is plain forest. That gives straight
east-west edges and puts jungle in the dry tropics.

**Plan:**
1. **Data.** Two sources:
   - **Köppen-Geiger climate zones at 1 km** (Beck et al. 2023, Scientific Data 10, 724), as a
     90 MB GeoTIFF from figshare. It sorts every square km into one of 30 climate zones
     (tropical rainforest, hot desert, humid continental, tundra and so on).
   - Optionally **CHELSA** monthly temperature and rainfall at 1 km (CC BY 4.0, Karger et al. 2017),
     for the seasons in goal 13.
   - Check the licence on both download pages before use. Both need credit on the website.
2. **Packing.** One tool turns the GeoTIFF into small tiles the mod can read a square at a time,
   like the elevation (`tools/PackElevation.java`). The planet at 1 km is 43,200 × 21,600 cells:
   one byte each, about 930 MB raw and roughly 50 MB packed. About an hour of work.
3. **The biome rule.** The climate zone chooses the family of biomes. Land cover then picks
   within it, and height then shifts it (mountains go colder):
   - Af/Am (rainforest) with trees → jungle; with shrubs or grass → sparse jungle or savanna.
   - Aw (savanna) → savanna; BWh/BWk (desert) → desert, with badlands on bare red rock if wanted.
   - BSh/BSk (steppe) → savanna or plains; Cs (Mediterranean) → a dry forest or plains mix.
   - Cf/Cw (temperate) → forest, birch forest, dark forest or plains, by cover.
   - Df/Dw (continental) → forest, taiga or snowy taiga, by how cold.
   - ET (tundra) → snowy plains; EF (ice cap) → ice spikes or frozen peaks.
   - A table in the code (`ClimateBiomes`) maps each of the 30 zones × cover to a biome. The
     biome list grows from 17 to about 30 vanilla biomes, which brings their own trees, grass
     colours and animals (and the Fauna table keeps working on top).
4. **Softer edges.** Climate cells are 1 km, or 200 blocks. To stop square edges, each biome lookup
   is shifted by a small fixed noise (±60 blocks) before reading the climate tile, the same trick
   the game uses.
5. **Check.** On the test server, generate the Amazon, the Sahel, the Sahara, Siberia, the Alps
   and Florida, and draw them with `tools/region_map.py`. Jungle should end where the rainforest
   ends, and the desert-to-savanna line should cross the Sahel at the right latitude, wobbling
   rather than straight.
6. **Size of the job:** one to two sessions. Risk: low. Biomes don't change the ground's shape,
   only its colours, plants and animals, so the change sits well next to old chunks.

## 2. Real land below sea level (goal 8)

**Now:** any land the map says is below sea level is raised to just above it, so the Dead Sea
shore, Death Valley, the Caspian depression, the Danakil and the Dutch polders are flat at y 161.

**The difficulty:** the elevation data can't tell "dry land at −30 m" from "sea floor at −30 m".
The land cover map says which is which, but along coasts the two disagree by a few hundred metres.
Those disagreements are what the current rule flattens on purpose.

**Plan:**
1. **A list of real depressions:** a small hand-made file with a box and the lowest level for each.
   About 25 entries covers almost every notable one:
   - the Dead Sea (−430 m)
   - the Jordan Valley
   - Lake Assal (−155 m)
   - the Danakil (−125 m)
   - the Qattara Depression (−133 m)
   - the Caspian depression
   - the Turpan basin (−154 m)
   - Death Valley (−86 m)
   - the Salton Sea (−69 m)
   - Laguna del Carbón (−105 m)
   - the Netherlands' polders (−7 m)
   - the Fens, Lammefjord, and the Lake Eyre basin.
2. **Inside a listed box,** land below sea level that is more than 2 km from the open sea keeps its
   real height. Water there (the Dead Sea, the Caspian, the Salton Sea, Lake Assal) stands at its
   own real level, not at the sea's. The lake machinery already does this for lakes above sea
   level; it just needs to accept levels below 160.
3. **Polders** (the Netherlands): the land stays at its real −2 to −7 m, which is 1 block below
   sea level. A dyke is built along the coast wherever such land touches the sea: a wall of stone
   and grass one block higher than the sea. Without it the sea would flow in.
4. **Caves and water:** `EarthFluids` already keeps dry land dry below sea level. Caves under a
   below-sea lake follow the same "8 blocks of seal" rule as now.
5. **Check:** the Dead Sea shore at y 74 and dry, the water at about y 74, Jericho's area dry at
   y 110 to 130. Death Valley's floor at y 143. Amsterdam's polders 1 block below the sea, behind a
   dyke, with no flooding after 10 minutes of game time.
6. **Size of the job:** one session. Risk: middle (water flowing where it shouldn't). The
   10-minute flood check covers it.

## 3. Live sky: real time of day and real weather (goal 12)

**What the game allows:** one time of day and one weather for the whole world, shared by every
player. Real "noon in Paris while it is night in Tokyo" can't be done for everyone at once with
an unmodified game, because the client draws the sky from the one world time it's sent.

**Plan (works with unmodified clients):**
- **Time of day per player:** the server already sends each player their own time packet. A
  small mixin can send each player the time of day for their own longitude, while the server's
  real clock keeps running normally for crops, mobs and spawning. Players far apart see different
  skies, exactly as wanted. Beds and phantoms follow the server's clock, not the sky: a known quirk
  to explain to players.
- **Weather per player:** the same idea. The rain and thunder packets are per player, so each
  player gets the weather at their position.
  - Real weather comes from a free service such as Open-Meteo (no key; its free use is
    non-commercial, so check that a server with a store counts).
  - It is asked for once every 15 minutes, for a grid of 2° squares, and only where players are:
    a few requests an hour.
  - The game's own rain on crops stays global (server weather off).
- **Size of the job:** two sessions. Risk: the game may resend the global time or weather in
  places the mixin misses (changing dimension, respawn). Those have to be hunted down on the test
  server with a real client.

## 4. Regional seasons (goal 13)

**What the game allows:** grass and leaf colour comes from the biome, so the server can change a
chunk's biome without touching blocks. Snow can be laid and melted as blocks.

**Plan:**
- Each month, each loaded area gets a "season variant" of its biome. A temperate forest becomes
  a snowy forest in January north of the equator and in July south of it. Tropics have a wet and
  dry season, which shows as greener and browner variants.
- The change applies to the biome data of chunks as they load (a mixin when a chunk is sent),
  never written to the world file. Turning the feature off leaves nothing behind, as goal 13 asks.
- Snow cover is laid on the surface as a chunk loads in winter, and melts in spring through the
  game's own snow ticking with a nudge. Water freezes in the same way.
- Uses the CHELSA monthly temperatures from section 1, so there's no extra data.
- **Size of the job:** two to three sessions, after section 1. Risk: middle. Clients must see the
  colours change without rejoining; a chunk resend on the month's turn handles that.

## 5. A sky page on earth.tj (goal 14)

Easy once 3 and 4 exist: a map page with a day/night shading line (computed in the browser), the
weather grid the server already fetches, and the season band. About half a session.

## 6. An economy driven by geography (goal 16)

**Plan:**
1. A written table: which ores, crops and animals belong to which real regions. For example:
   - copper in Chile and Zambia, iron in Australia and Brazil, gold in South Africa and Nevada,
     diamonds in Botswana, coal in Appalachia and the Ruhr
   - wheat on the plains, rice in East and South Asia, cocoa in West Africa
   - sheep in New Zealand, cattle in Argentina.

   The owner approves the table before anything is built.
2. **Ores:** the existing ore placement (`HeightRangePlacementMixin`) gets a regional multiplier,
   for example ×3 copper in the copper belt and ×0.3 elsewhere. The totals over the world stay as
   in the ordinary game, so nothing becomes impossible, only cheaper in the right place.
3. **Crops:** growth speed by region through a mixin on crop growth: native crops grow at the
   normal rate, others at half. Villager trades in a region favour its goods.
4. **Trade:** a wrapper command and a website page listing regional prices, updated from what
   players actually sell. This is the part to design with the owner, because it touches Vote
   Points.
5. **Size of the job:** the table (half a session, then the owner's review) plus two sessions to
   build.

## 7. Vegetation of a region (goal 19)

- **First:** giant sequoias in the Sierra Nevada (36–38.5°N, 118.5–119.5°W, 1,400–2,100 m), using
  the game's mega spruce shape at double height with a dark oak and spruce trunk.
- **Then a list for the owner to extend:**
  - baobabs in the Sahel and Madagascar
  - eucalyptus (birch-like) in Australia
  - cherry blossom in Japan, which the game already has as a biome
  - cacti only in the Americas
  - olive-like trees round the Mediterranean
  - mangroves where the land cover already says so.
- **How:** a "regional trees" placed feature that runs after the normal trees in the listed
  boxes, plus the same Fauna-style table for which vanilla trees are kept or removed in a region.
- **Size of the job:** one session for the mechanism and sequoias, then a little per species.

## 8. The rest of goal 17 (cities)

After the Baltimore and Moscow trial:
- **Pack the planet's buildings:** about 2.7 billion outlines in Overture.
  - Each one-degree tile is packed on its own. About 15,000 tiles have any buildings.
  - The pack is roughly 200–400 GB, comparable to the elevation, and is fetched tile by tile over
    a few days, rate-limited like the earlier downloads.
  - **Disk:** check free space first. The packed elevation already takes 132 GB, and 190 GB of raw
    elevation downloads could be deleted if the owner agrees.
- **Walls and roofs by region:**
  - brick in northern Europe
  - stucco and terracotta round the Mediterranean
  - concrete and glass for tall buildings everywhere
  - timber in Scandinavia and North America's suburbs.
- **Homes and jobs for villagers:** a bed in a residential building near each villager, and a job
  block in a commercial one.
- **A find-my-address command:** `!find` already does addresses through OpenStreetMap search, so
  this is mostly done.
- **Keep buildings out from under monuments:** done by the monument placer, which clears its own
  footprint.

## 9. Still to decide: where new players start (goal 10)

Today everyone starts at Baltimore, my provisional pick. Options:
- (a) Baltimore for everyone
- (b) a choice of a few hub cities on first join (London, New York, Tokyo, Sydney, Cairo) through
  a sign menu
- (c) a random big city.

This is the owner's call.
