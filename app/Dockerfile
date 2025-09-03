FROM python:3.12

# Update system packages to latest security patches
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        gcc \
        libxslt1-dev \
        libxml2-dev \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install the application dependencies
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the remaining source code
COPY . ./

# Expose the port your app will be on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
