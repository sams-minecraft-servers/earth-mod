package tj.earth.worldgen;

import java.io.IOException;
import java.nio.ShortBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.concurrent.ConcurrentHashMap;

/**
 * The height of the real ground, in metres above sea level, from one-degree elevation tiles
 * (SRTM ".hgt": a square grid of big-endian 16-bit metres, north row first). Tiles are mapped
 * into memory the first time a chunk needs them, so only places being explored cost anything.
 */
public final class Elevation {
    private static final short VOID = Short.MIN_VALUE;
    private static final Tile MISSING = new Tile(null, 0);
    private static final ConcurrentHashMap<Integer, Tile> TILES = new ConcurrentHashMap<>();

    private record Tile(ShortBuffer metres, int size) {}

    private Elevation() {}

    /** Metres above sea level at a point, or NaN where nothing is known (open sea, a gap in the data). */
    public static float metres(double latitude, double longitude) {
        if (latitude >= 90 || latitude <= -90) return Float.NaN;
        longitude = ((longitude + 180) % 360 + 360) % 360 - 180;
        int south = (int) Math.floor(latitude), west = (int) Math.floor(longitude);
        Tile tile = TILES.computeIfAbsent(south * 1000 + west, key -> load(south, west));
        if (tile == MISSING) return Float.NaN;

        int last = tile.size - 1;
        double column = (longitude - west) * last, row = (south + 1 - latitude) * last;
        int c = Math.min((int) column, last - 1), r = Math.min((int) row, last - 1);
        float fx = (float) (column - c), fy = (float) (row - r);
        ShortBuffer m = tile.metres;
        short a = m.get(r * tile.size + c), b = m.get(r * tile.size + c + 1);
        short d = m.get((r + 1) * tile.size + c), e = m.get((r + 1) * tile.size + c + 1);
        if (a == VOID || b == VOID || d == VOID || e == VOID) return Float.NaN;
        float top = a + (b - a) * fx, bottom = d + (e - d) * fx;
        return top + (bottom - top) * fy;
    }

    private static Tile load(int south, int west) {
        String name = String.format("%c%02d%c%03d.hgt", south < 0 ? 'S' : 'N', Math.abs(south), west < 0 ? 'W' : 'E', Math.abs(west));
        Path file = Path.of(EarthConfig.get().dataDir, name);
        if (!Files.exists(file)) return MISSING;
        try (FileChannel channel = FileChannel.open(file, StandardOpenOption.READ)) {
            long samples = channel.size() / 2;
            int size = (int) Math.round(Math.sqrt(samples));
            if ((long) size * size != samples || size < 2) throw new IOException("not a square grid of 16-bit heights");
            return new Tile(channel.map(FileChannel.MapMode.READ_ONLY, 0, channel.size()).asShortBuffer(), size);
        } catch (IOException e) {
            EarthWorldgen.LOG.error("Earth: elevation tile {} could not be used: {}", file, e.getMessage());
            return MISSING;
        }
    }
}
