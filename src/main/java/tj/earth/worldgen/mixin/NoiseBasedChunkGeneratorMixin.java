package tj.earth.worldgen.mixin;

import net.minecraft.core.Holder;
import net.minecraft.world.level.chunk.ChunkAccess;
import net.minecraft.world.level.levelgen.Aquifer;
import net.minecraft.world.level.levelgen.NoiseBasedChunkGenerator;
import net.minecraft.world.level.levelgen.NoiseChunk;
import net.minecraft.world.level.levelgen.NoiseGeneratorSettings;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import tj.earth.worldgen.EarthFill;
import tj.earth.worldgen.EarthFluids;

/**
 * Gives the Earth dimension its own rule for where water stands (see EarthFluids) and its own, much
 * shorter, way of turning the noise settings into blocks (see EarthFill). Other dimensions are untouched.
 */
@Mixin(NoiseBasedChunkGenerator.class)
abstract class NoiseBasedChunkGeneratorMixin {
    @Shadow @Final
    private Holder<NoiseGeneratorSettings> settings;

    @Inject(method = "doFill", at = @At("HEAD"), cancellable = true)
    private void earth$fill(final NoiseChunk noiseChunk, final ChunkAccess chunk, final CallbackInfo callback) {
        NoiseGeneratorSettings settings = this.settings.value();
        if (EarthFluids.isEarth(settings)) {
            EarthFill.fill(settings, noiseChunk, chunk);
            callback.cancel();
        }
    }

    @Inject(method = "createFluidPicker", at = @At("HEAD"), cancellable = true)
    private static void earth$fluids(final NoiseGeneratorSettings settings, final CallbackInfoReturnable<Aquifer.FluidPicker> callback) {
        if (EarthFluids.isEarth(settings)) callback.setReturnValue(EarthFluids.picker(settings));
    }
}
