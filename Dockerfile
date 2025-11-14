FROM ubuntu:latest
LABEL authors="xhome"

ENTRYPOINT ["top", "-b"]