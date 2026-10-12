package tj.earth.worldgen;

import com.google.gson.Gson;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Path;

/**
 * How the real Earth is laid onto the world. Read once from config/earth_worldgen.json in the
 * server's folder; a missing file or field means the default below.
 *
 * Changing any of these after a world has been explored leaves a seam between old and new chunks.
 */
public final class EarthConfig {
    /** Folder of elevation tiles (N44E008.hgt and so on). */
    public String dataDir = "earth-data/hgt";
    /** Real metres across one block on the ground, at the equator: 5 means a 1:5 map. */
    public double horizontalScale = 5.0;
    /**
     * Real metres of height in one block. Less than horizontalScale exaggerates the relief.
     * The world is 4064 blocks tall and the Earth spans 19,784 m from its deepest trench to its
     * highest peak, so nothing under about 4.9 fits; 5 is true scale on a 1:5 map.
     */
    public double metresPerBlockY = 5.0;
    /**
     * Must be the same as sea_level in the datapack's noise settings. At 160, with 5 m per block,
     * Everest (y 1930) and the Challenger Deep (y -2027) are both inside the world.
     */
    public int seaLevel = 160;
    /** How far below sea level the seabed lies where no depth is known, in blocks. */
    public int unknownSeaDepth = 6;

    private static final double EQUATOR_METRES = 40_075_016.686;
    private static EarthConfig instance;

    public static synchronized EarthConfig get() {
        if (instance == null) {
            Path file = Path.of("config", "earth_worldgen.json");
            EarthConfig loaded = null;
            if (Files.exists(file)) {
                try (Reader in = Files.newBufferedReader(file)) {
                    loaded = new Gson().fromJson(in, EarthConfig.class);
                } catch (Exception e) {
                    throw new IllegalStateException("config/earth_worldgen.json could not be read: " + e.getMessage(), e);
                }
            }
            instance = loaded != null ? loaded : new EarthConfig();
            EarthWorldgen.LOG.info("Earth: 1:{} map, {} m of height per block, elevation from {}",
                (long) instance.horizontalScale, instance.metresPerBlockY, Path.of(instance.dataDir).toAbsolutePath());
        }
        return instance;
    }

    /** Blocks in one degree of longitude, and (the map is a plain grid) of latitude. */
    public double blocksPerDegree() {
        return EQUATOR_METRES / horizontalScale / 360.0;
    }

    public double latitude(int blockZ) {
        return -blockZ / blocksPerDegree();
    }

    public double longitude(int blockX) {
        return blockX / blocksPerDegree();
    }
}
