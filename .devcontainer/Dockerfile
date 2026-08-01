FROM mcr.microsoft.com/devcontainers/python:3

RUN python -m pip install --upgrade pip \
    && python -m pip install 'flit>=3.8.0'\
    && python -m pip install pre-commit

ENV FLIT_ROOT_INSTALL=1

COPY pyproject.toml .
RUN touch README.md \
    && mkdir -p src/mtdx62_mb \
    && python -m flit install --only-deps --deps develop \
    && rm -r pyproject.toml README.md src

# Add user to dialout group to allow access to serial ports
RUN sudo usermod -aG dialout vscode
