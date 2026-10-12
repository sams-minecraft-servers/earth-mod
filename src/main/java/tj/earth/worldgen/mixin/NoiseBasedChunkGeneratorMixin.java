package tj.earth.worldgen.mixin;

import net.minecraft.world.level.levelgen.Aquifer;
import net.minecraft.world.level.levelgen.NoiseBasedChunkGenerator;
import net.minecraft.world.level.levelgen.NoiseGeneratorSettings;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import tj.earth.worldgen.EarthFluids;

/** Gives the Earth dimension its own rule for where water stands (see EarthFluids). Other dimensions are untouched. */
@Mixin(NoiseBasedChunkGenerator.class)
abstract class NoiseBasedChunkGeneratorMixin {
    @Inject(method = "createFluidPicker", at = @At("HEAD"), cancellable = true)
    private static void earth$fluids(final NoiseGeneratorSettings settings, final CallbackInfoReturnable<Aquifer.FluidPicker> callback) {
        if (EarthFluids.isEarth(settings)) callback.setReturnValue(EarthFluids.picker(settings));
    }
}
