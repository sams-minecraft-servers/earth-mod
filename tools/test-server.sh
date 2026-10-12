#!/usr/bin/env bash
# Runs the throwaway test server in run/ (never one of the live servers), feeds it the console
# commands in the given file once it has started, then stops it.
#
#   tools/test-server.sh commands.txt [--fresh]     --fresh deletes the test world first
#
# In the commands file a line "wait 20" pauses for that many seconds.
set -euo pipefail
cd "$(dirname "$0")/.."
COMMANDS=${1:?usage: tools/test-server.sh commands.txt [--fresh]}
RUN=run
[ -s "$RUN/fabric-server.jar" ] || { echo "run/fabric-server.jar is missing (see README)"; exit 1; }
if [ "${2:-}" = "--fresh" ]; then find "$RUN/world" -mindepth 1 -maxdepth 1 ! -name datapacks -exec rm -r {} +; fi

mkdir -p "$RUN/mods" "$RUN/config" "$RUN/world/datapacks"
find "$RUN/mods" -name 'earth-worldgen-*.jar' -delete
cp build/libs/earth-worldgen-*.jar "$RUN/mods/"
rm -rf "$RUN/world/datapacks/earth" && cp -r datapack "$RUN/world/datapacks/earth"
[ -f "$RUN/config/earth_worldgen.json" ] || cp config.example.json "$RUN/config/earth_worldgen.json"
echo "eula=true" > "$RUN/eula.txt"
[ -f "$RUN/server.properties" ] || cat > "$RUN/server.properties" <<'PROPS'
server-ip=127.0.0.1
server-port=25599
level-name=world
motd=Earth worldgen test
online-mode=true
view-distance=6
simulation-distance=4
spawn-protection=0
enable-rcon=false
sync-chunk-writes=false
PROPS

FIFO=$(mktemp -u) && mkfifo "$FIFO"
trap 'rm -f "$FIFO"' EXIT
( cd "$RUN" && exec java -Xmx${TEST_HEAP:-4G} -Xms1G -jar fabric-server.jar --nogui < "$FIFO" > server.out 2>&1 ) &
SERVER=$!
exec 3> "$FIFO"
for i in $(seq 1 180); do
    grep -q 'Done (' "$RUN/server.out" && break
    kill -0 $SERVER 2>/dev/null || { echo "the server stopped while starting:"; tail -40 "$RUN/server.out"; exit 1; }
    sleep 1
done
grep -q 'Done (' "$RUN/server.out" || { echo "the server did not finish starting:"; tail -40 "$RUN/server.out"; kill $SERVER; exit 1; }
while IFS= read -r line; do
    case "$line" in
        ''|'#'*) ;;
        wait\ *) sleep "${line#wait }" ;;
        *) echo "$line" >&3 ;;
    esac
done < "$COMMANDS"
echo "stop" >&3
exec 3>&-
wait $SERVER || true
