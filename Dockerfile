FROM debian:stretch

# install ruby dependencies
RUN apt-get update && apt-get install -y \
      build-essential \
      gcc-arm-linux-gnueabi \
      sox \
      wget \
      mplayer
