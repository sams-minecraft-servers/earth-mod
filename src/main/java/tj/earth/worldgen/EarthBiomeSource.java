package tj.earth.worldgen;

import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.stream.Stream;
import net.minecraft.core.Holder;
import net.minecraft.core.HolderGetter;
import net.minecraft.core.QuartPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.RegistryOps;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.BiomeResolver;
import net.minecraft.world.level.biome.BiomeSource;
import net.minecraft.world.level.biome.Biomes;
import net.minecraft.world.level.biome.Climate;

/**
 * "earth_worldgen:earth" for the datapack's dimension: the biome of each place, from where it is
 * on the real Earth. For now that is its height and latitude only; land cover and climate follow.
 */
public final class EarthBiomeSource extends BiomeSource {
    public static final MapCodec<EarthBiomeSource> CODEC = RecordCodecBuilder.mapCodec(
        i -> i.group(RegistryOps.retrieveGetter(Registries.BIOME)).apply(i, i.stable(EarthBiomeSource::new)));

    private final Holder<Biome> ocean, beach, plains, forest, taiga, meadow, stonyPeaks, frozenPeaks;

    private EarthBiomeSource(final HolderGetter<Biome> biomes) {
        this.ocean = biomes.getOrThrow(Biomes.OCEAN);
        this.beach = biomes.getOrThrow(Biomes.BEACH);
        this.plains = biomes.getOrThrow(Biomes.PLAINS);
        this.forest = biomes.getOrThrow(Biomes.FOREST);
        this.taiga = biomes.getOrThrow(Biomes.TAIGA);
        this.meadow = biomes.getOrThrow(Biomes.MEADOW);
        this.stonyPeaks = biomes.getOrThrow(Biomes.STONY_PEAKS);
        this.frozenPeaks = biomes.getOrThrow(Biomes.FROZEN_PEAKS);
    }

    @Override
    protected Stream<Holder<Biome>> collectPossibleBiomes() {
        return Stream.of(ocean, beach, plains, forest, taiga, meadow, stonyPeaks, frozenPeaks);
    }

    @Override
    protected MapCodec<EarthBiomeSource> codec() {
        return CODEC;
    }

    @Override
    public BiomeResolver createResolver(final Climate.Sampler sampler) {
        return (quartX, quartY, quartZ) -> biomeAt(QuartPos.toBlock(quartX) + 2, QuartPos.toBlock(quartZ) + 2);
    }

    private Holder<Biome> biomeAt(final int blockX, final int blockZ) {
        float metres = Terrain.metres(blockX, blockZ);
        if (Terrain.isSea(metres)) return ocean;
        double latitude = Math.abs(EarthConfig.get().latitude(blockZ));
        // Roughly where permanent snow and the last trees are found: lower towards the poles.
        double snowLine = Math.max(0, 5000 - 48 * latitude), treeLine = snowLine - 900;
        if (metres > snowLine) return frozenPeaks;
        if (metres > treeLine + 400) return stonyPeaks;
        if (metres > treeLine) return meadow;
        if (metres > treeLine - 900) return taiga;
        if (metres < 3) return beach;
        return metres > 350 ? forest : plains;
    }
}
