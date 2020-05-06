# Brandmeister bridge to mumble

Stream Brandmeister DMR calls using the Open DMR
terminal protocol. This connects a BrandMeister
DMR talkgroup to a Mumble bot user, enableing
people to listen to a DMR talkgroup without a
radio.

Mumble is a free, open source, low latency, high
quality voice chat application. It can handle
massive amounts of concurrent users.

## Command

Stream Talkgroup audio to a fifo:
`./dmr-brandmeister | python2 decode72to49.py | python3 to_ambe_format_file.py | qemu-arm md380tools/emulator/md380-emu -d | sox --buffer 256 -r 8000 -e signed-integer -L -b 16 -c 1 -t raw /dev/stdin -t raw -r 48000 /tmp/dmr.fifo reverb`

## Setup

- Build the Go application with `go build`, this results in a `dmr-brandmeister` binary
- Fill out `config.json` from `config-example.json`
- Make a Python2 virtualenv in `venv` and pip-install `bitstring` and `bitarray`. Activate the virtualenv.
- Install `python3`
- Clone the [md380 tools](https://github.com/travisgoodspeed/md380tools) repository and compile the emulator. If you don't want to set up the cross-compiler, use the Dockerfile:
  - `docker build -t debian .`
  - `docker run --rm -it --mount src=$(pwd)/md380tools,target=/md380tools,type=bind debian /bin/bash`
  - (In this shell): `cd /md380tools/emulator && make md380-emu`. Then leave the shell.
  - This will have built an ARM binary that encodes and decodes the AMBE codec.
- Install `sox`
- Install ruby and the `mumble-ruby` gem

## Software used

- the tool that talks to the BrandMeister network was adapted from [callrec](https://github.com/BrandMeister/callrec)
- `decode49to70.py` is adapted from [dmr_utils](https://github.com/n0mjs710/dmr_utils/)

## Explanation of stages

### `./dmr-brandmeister`

This talks to the BrandMeister network,
subscribes to the configured talkgroups and
prints three concatenated forwared-error-
corrected AMBE packets to stdout. Each packet is
72 bits long.

### `python2 decode72to49.py`

This takes the concatenated forwared-error-
corrected AMBE packets on stdin, splits them,
hex decodes them and then removes the FEC, leaving
only the ABME packets (these are 49 bits long)
and printing them, hex encoded, to stdout.

This step converts the 3600 bits per second to
2450 bits per second.

### `python3 to_ambe_format_file.py`

This takes the hex-encoded AMBE-packets and prints
them out in the `.amb` format DSD and md380 tools
use. This is the first step in the pipeline where
the output is binary.

### `qemu-arm md380tools/emulator/md380-emu -d`

This emulates the firmware of the MD380 radio,
decoding the AMBE stream on stdin to stdout.

### `sox --buffer 256 -r 8000 -e signed-integer -L -b 16 -c 1 -t raw /dev/stdin -t raw -r 48000 /tmp/dmr.fifo reverb`

This takes the raw decoded stream on stdin,
upsamples it from 8000 bits per second to 48000
and applies a reverb effect. It then writes this
PCM stream to the `/tmp/dmr.fifo` steam, ready
for the mumble bridge to pick it up.

## Legal (I'm not a lawyer)

The AMBE codec is [still under patent until 2023-11-07](https://patents.google.com/patent/EP1420390B1/en). This means that using the AMBE decoder/encoder might not be legal where you live.

In my country (Belgium), the rights coming from patents don't apply for actions in the
private sphere that are non-commercial ([source](https://economie.fgov.be/nl/themas/intellectuele-eigendom/octrooien/beperkingen-en-uitzonderingen)).
There are also laws prohibiting
from doing any commercial actions on the amateur
radio bands. The code that handles the AMBE
encoding and decoding is also not in this
repository: it is in the
[md380 tools](https://github.com/travisgoodspeed/md380tools) repository. In this repository, I am
only talking about how to use the md380 software, which
is protected under free speech (I think, again,
  I'm not a lawyer).

If you want to be absolutely sure you're not
infringing any patents, use an AMBE decoder USB
dongle.