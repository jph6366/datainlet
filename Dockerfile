FROM pdal/pdal

USER root
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

USER pdal
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Create a data directory and set ownership
RUN mkdir -p $HOME/app/

# Set the working directory
WORKDIR $HOME/app

RUN git clone https://github.com/jph6366/datainlet.git .

RUN mkdir -p data 

# Sync the dependencies
RUN [ "uv", "sync" ]

# Run the Dagster server
CMD [ "uv", "run", "dagster-webserver", "--read-only", "-h", "0.0.0.0", "-p", "7860" ]