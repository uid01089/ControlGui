FROM arm64v8/python:3.12-slim


# Update system
RUN apt-get update -q \
  && apt-get install --no-install-recommends -qy g++ gcc inetutils-ping

# Create workdir
WORKDIR /app

RUN mkdir /data

# Setup requirements, no venv needed
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Clean up
RUN apt-get remove -qy g++ gcc --purge

# Copy app itself
COPY . .

# Call script
CMD [ "python", "./ControlGui.py" ]
