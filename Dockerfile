FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/lib
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    lsb-release \
    ca-certificates \
    cmake \
    git \
    libgdal-dev \
    ninja-build \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN git clone -b stable --depth 1 https://github.com/PDAL/PDAL.git

WORKDIR /PDAL

RUN mkdir build && \
    cd build && \
    cmake -G Ninja -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_INSTALL_LIBDIR=lib .. \
    ninja && \
    ninja install

RUN pip install --upgrade pip

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Copy the datadex project and dependencies
RUN git clone https://github.com/jph6366/datainlet.git $HOME/app && \
    cd $HOME/app && \
    chown -R user:user .

# Create a data directory and set ownership
RUN mkdir -p $HOME/app/data && chown -R user:user $HOME/app/data

# Set the working directory
WORKDIR $HOME/app

# Sync the dependencies
RUN [ "uv", "sync" ]

# Run the Dagster server
CMD [ "uv", "run", "dagster-webserver", "--read-only", "-h", "0.0.0.0", "-p", "7860" ]