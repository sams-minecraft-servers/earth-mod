package tj.earth.worldgen.mixin;

import net.minecraft.world.level.StructureManager;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.chunk.ChunkAccess;
import net.minecraft.world.level.chunk.ChunkGenerator;
import net.minecraft.world.level.dimension.DimensionType;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import tj.earth.worldgen.UrbanBuilder;

/**
 * Builds the real streets and buildings into each chunk of the Earth dimension (see UrbanBuilder)
 * just before the game adds its trees, plants and structures. Other dimensions are untouched.
 */
@Mixin(ChunkGenerator.class)
abstract class ChunkGeneratorMixin {
    @Inject(method = "applyBiomeDecoration", at = @At("HEAD"))
    private void earth$streets(final WorldGenLevel level, final ChunkAccess chunk, final StructureManager structureManager, final CallbackInfo callback) {
        if (chunk.getHeight() == DimensionType.Y_SIZE) UrbanBuilder.build(chunk);
    }
}
