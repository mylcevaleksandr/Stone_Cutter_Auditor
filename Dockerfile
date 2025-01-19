# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the stone_cutter directory to the container
COPY . /app

# Install any dependencies from requirements.txt and create a virtual environment
RUN python -m venv venv && /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

# Run the Python script (assuming bot.py is the main script)
CMD ["python", "bot.py"]
