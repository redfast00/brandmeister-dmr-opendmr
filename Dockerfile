FROM debian:stretch

RUN apt-get update && apt-get install -y \
      build-essential gcc-arm-linux-gnueabi unzip \
      sox \
      wget \
      mplayer
