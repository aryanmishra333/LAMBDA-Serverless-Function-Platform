FROM ubuntu:22.04

# Set environment to non-interactive to avoid timezone prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install Icarus Verilog and dependencies
RUN apt-get update && apt-get install -y \
    iverilog \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY docker/polar_codec.v /app/code.v
CMD ["/bin/bash", "-c", "iverilog -o /app/output /app/code.v && /app/output"]