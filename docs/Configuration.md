# Configuration

The mod reads `config/earth_worldgen.json` in the server's folder once, at start-up. Any missing
setting (or a missing file) uses the default below. Relative paths are read from the server's folder.

```json
{
  "dataDir": "earth-data/elevation",
  "landCoverDir": "earth-data/worldcover",
  "urbanDir": "earth-data/urban",
  "horizontalScale": 5,
  "metresPerBlockY": 5,
  "seaLevel": 160,
  "unknownSeaDepth": 6,
  "villagersPerCityChunk": 0.25
}
```

> **Decide before players explore.** Changing the scale, heights or sea level after chunks exist
> leaves visible seams between old and new land, because existing chunks are never remade.

| Setting | Default | Meaning |
|---|---|---|
| `dataDir` | `earth-data/elevation` | Folder of packed elevation tiles (`N44/N44E008.ehg`, …). A missing tile is open sea. |
| `landCoverDir` | `earth-data/worldcover` | Folder of ESA WorldCover GeoTIFFs. Without them, biomes go by height and latitude only, there are no inland lakes or rivers, and land below sea level floods. |
| `urbanDir` | `earth-data/urban` | Folder of packed streets and buildings (`N44/N44E008.urb`, …). Nothing is built where a tile is missing; point it at a folder that doesn't exist to turn buildings off. |
| `horizontalScale` | `5` | Real metres per block on the ground, at the equator. `5` is a 1:5 map. |
| `metresPerBlockY` | `5` | Real metres of height per block. Lower values exaggerate the relief. |
| `seaLevel` | `160` | The Y of the sea. **Must match `sea_level` in the datapack's noise settings** (`datapack/data/earth_worldgen/worldgen/noise_settings/earth.json`). |
| `unknownSeaDepth` | `6` | How many blocks below sea level the sea bed lies where the data gives no depth. |
| `villagersPerCityChunk` | `0.25` | Villagers placed in each chunk of built-up land when it is first made. A half built-up chunk gets half. `0` for none. |

## Choosing a scale

The map is a plain grid: one degree of longitude and one degree of latitude are the same number of
blocks, `40,075,016.686 / horizontalScale / 360`. At 1:5 that is about 22,264 blocks per degree,
so the world runs from X −4,007,502 to 4,007,502 and Z −2,003,751 to 2,003,751.

- **Smaller numbers make a bigger world.** 1:1 is about 20 million blocks either side of block 0,
  inside the game's 30 million limit. Bigger worlds take longer to cross and need more disk for
  the world. Above 5, houses and streets become too small to show as more than a block.
- **Height has a floor.** The world is 4,064 blocks tall and the Earth's relief, trench to peak, is
  19,784 m, so `metresPerBlockY` below about 4.9 can't fit both Everest and the deepest trenches.
  With a small horizontal scale, keep this at 5: the land then looks flatter than in reality,
  because heights are shrunk more than distances.
- With the defaults, Everest's summit is at Y 1930 and the Challenger Deep at Y −2027.
