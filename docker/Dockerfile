FROM python:3.9-slim

# Set the working directory
WORKDIR /app

#Install dependencies for paramiko
RUN apt-get update && apt-get install -y  \
    libffi-dev libssl-dev  gcc make build-essential openssh-client \ 
    && rm -rf /var/lib/apt/lists/*


#Copy the requirements file
COPY requirements.txt /app/requirements.txt

#Install the dependencies for Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

#Copy the source code
COPY . /app

#Code lintin and testing
RUN make lint
RUN make test

#Expose the port
EXPOSE 8000

#Run the application from main.py
CMD ["python", "main.py"]