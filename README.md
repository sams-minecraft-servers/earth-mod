# Earth worldgen

A Fabric mod (server side only; players join with an unmodified game) that generates the real
Earth as chunks are first needed, from elevation data, instead of from a pre-generated map.

- `src/` the mod: `earth_worldgen:surface` (density function: the Y of the real ground at a column)
  and `earth_worldgen:earth` (biome source). No Fabric API; one mixin registers its types.
- `datapack/` goes in the world's `datapacks/` folder **before the world is first started**. It makes
  the overworld 4064 blocks tall (Y -2032 to 2031, the most the game allows) and points its
  generator at the mod.
- `config.example.json` becomes `config/earth_worldgen.json` in the server's folder: map scale,
  metres of height per block, where the elevation tiles are.
- Elevation tiles are one-degree SRTM `.hgt` files (they include sea depths), e.g. from
  `https://s3.amazonaws.com/elevation-tiles-prod/skadi/N45/N45E006.hgt.gz`. A missing tile is open sea.

## Building and trying it

    tools/guard.sh 4G ./gradlew build --no-daemon    # build/libs/earth-worldgen-<version>.jar
    tools/test-server.sh commands.txt --fresh        # a private server in run/ on 127.0.0.1:25599
    tools/region_map.py run/world/dimensions/minecraft/overworld/region out.png

`run/` needs `fabric-server.jar` (the Fabric server launcher for this Minecraft version, from
https://fabricmc.net/use/server/). The test server is never one of the live servers.

## Moving to a new Minecraft version

1. Change `minecraft_version`, `loader_version` and `loom_version` in `gradle.properties`.
2. `./gradlew build`. World generation internals change often: fix what no longer compiles
   (`./gradlew genSources` gives readable game sources to compare against).
3. Compare `datapack/` with the new version's own `dimension_type/overworld.json` and
   `worldgen/noise_settings/overworld.json`, and update `pack.mcmeta`.
4. Run the test server on a copy of the world before the live server is updated.
