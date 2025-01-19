# Use the official Python image as the base image
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the stone_cutter directory to the container
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the Python script (assuming bot.py is the main script)
CMD ["python", "bot.py"]
