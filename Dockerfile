FROM ubuntu:latest


WORKDIR /workspace

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    pipx \
    libglfw3 \
    libgl1-mesa-glx \
    libosmesa6-dev \
    libglew-dev \
    patchelf \
    wget \
    unzip \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*


# Install poetry using pipx
RUN pipx ensurepath
RUN pipx install poetry
RUN pipx ensurepath

# # Set up MuJoCo
# RUN mkdir -p /root/.mujoco \
#     && wget -qO- https://mujoco.org/download/mujoco210-linux-x86_64.tar.gz | tar -xvz -C /root/.mujoco

ENV MUJOCO_GL="osmesa"
ENV MUJOCO_PATH="/root/.mujoco/mujoco210"
ENV LD_LIBRARY_PATH="$MUJOCO_PATH/bin:$LD_LIBRARY_PATH"

# # Copy project files and install dependencies using Poetry
# WORKDIR /home/user
# COPY . /home/user
# RUN poetry install --no-root

# Add user and switch to non-root
# RUN useradd -ms /bin/bash user
# USER user
# WORKDIR /home/user

# Set environment variable to disable file validation in debugger
# ENV PYDEVD_DISABLE_FILE_VALIDATION=1

CMD ["bash"]