package tj.earth.worldgen;

/** Where the surface of the world is, and what kind of place it is, for one column of blocks. */
public final class Terrain {
    private Terrain() {}

    /** Real metres above sea level at a column; NaN or not above zero means water. */
    public static float metres(int blockX, int blockZ) {
        EarthConfig c = EarthConfig.get();
        return Elevation.metres(c.latitude(blockZ), c.longitude(blockX));
    }

    public static boolean isSea(float metres) {
        return !(metres > 0);
    }

    /** The Y just above the top solid block of a column: blocks below it are ground. */
    public static float surfaceY(int blockX, int blockZ) {
        EarthConfig c = EarthConfig.get();
        float metres = metres(blockX, blockZ);
        if (Float.isNaN(metres)) return c.seaLevel - c.unknownSeaDepth;
        // The seabed, with at least a block of water over it; the deepest trenches stop short of the world's floor.
        if (isSea(metres)) return (float) Math.max(c.seaLevel - 1 + metres / c.metresPerBlockY, net.minecraft.world.level.dimension.DimensionType.MIN_Y + 32);
        // Land is never awash: the lowest shore stands one block clear of the water.
        return (float) (c.seaLevel + 1 + metres / c.metresPerBlockY);
    }
}
