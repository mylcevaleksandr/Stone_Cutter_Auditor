# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the stone_cutter directory to the container
COPY . /app

# Create a virtual environment without ensurepip
RUN python -m venv venv --without-pip

# Activate the virtual environment and install pip using get-pip.py
RUN /bin/bash -c "source venv/bin/activate && curl https://bootstrap.pypa.io/get-pip.py | python"

# Install dependencies from requirements.txt within the virtual environment
RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

# Run the Python script (assuming bot.py is the main script)
CMD ["python", "bot.py"]
