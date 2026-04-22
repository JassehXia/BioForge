# 1. Start with a lightweight Linux base (Ubuntu 22.04)
FROM ubuntu:22.04

# 2. Tell the installer not to ask us questions (non-interactive)
ENV DEBIAN_FRONTEND=noninteractive

# 3. Install the AutoDock Vina binary and Python dependencies
RUN apt-get update && apt-get install -y \
    autodock-vina \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 4. Set our home base inside the container
WORKDIR /app

# 5. When we start the container, check if Vina is alive
CMD ["vina", "--version"]
