# Use latest official uv image
FROM ghcr.io/astral-sh/uv:debian-slim

# Set working directory to /app
WORKDIR /app

# Copy pyproject.toml, lockfile, and runfile
COPY pyproject.toml uv.lock ./run ./

# Build environment
RUN ["./run", "restore"]

# Copy everything else into the container
COPY . .

# Run service
CMD ["./run", "serve"]
