FROM ubuntu:20.04

# Install system updates and tools
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt-get install -y --no-install-recommends \
    ca-certificates \
    postfix && \
# Clean up & back to dialog front end
    apt autoremove -y && \
    apt clean -y && \
    rm -rf /var/lib/apt/lists/*
ENV DEBIAN_FRONTEND=dialog

COPY start-postfix.sh /usr/local/bin/start-postfix
RUN  chmod +x /usr/local/bin/start-postfix

# Set LANG environment
ENV LANG C.UTF-8

# open SMTP port in the container
EXPOSE 25

# prepare postfix config and start it in foreground
CMD ["start-postfix"]
