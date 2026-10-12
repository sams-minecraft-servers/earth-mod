package tj.earth.worldgen;

import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.dimension.DimensionType;
import net.minecraft.world.level.levelgen.Aquifer;
import net.minecraft.world.level.levelgen.NoiseGeneratorSettings;

/**
 * Where water goes. The game's own rule is one sea level for the whole world, with lava below
 * Y -54; here the sea is at sea level, each lake and river stands at its real height, land below
 * sea level stays dry, and the ocean deeps are water all the way down.
 */
public final class EarthFluids {
    private static final Aquifer.FluidStatus NONE = new Aquifer.FluidStatus(Terrain.DRY, Blocks.AIR.defaultBlockState());

    /** The answer for the column a thread asked about last: the game asks once per block, top to bottom. */
    private static final class Last {
        int x = Integer.MIN_VALUE, z;
        Aquifer.FluidStatus status;
    }

    private EarthFluids() {}

    /** Our dimension is the one that uses the full height the game allows. */
    public static boolean isEarth(final NoiseGeneratorSettings settings) {
        return settings.noiseSettings().height() == DimensionType.Y_SIZE;
    }

    public static Aquifer.FluidPicker picker(final NoiseGeneratorSettings settings) {
        final ThreadLocal<Last> last = ThreadLocal.withInitial(Last::new);
        final Aquifer.FluidStatus sea = new Aquifer.FluidStatus(settings.seaLevel(), settings.defaultFluid());
        return (x, y, z) -> {
            Last l = last.get();
            if (l.x != x || l.z != z || l.status == null) {
                int level = Terrain.waterLevel(x, z);
                l.x = x;
                l.z = z;
                l.status = level == Terrain.DRY ? NONE : level == settings.seaLevel() ? sea : new Aquifer.FluidStatus(level, settings.defaultFluid());
            }
            return l.status;
        };
    }
}
