# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variables
ENV TEST_PROGRAM=false
ENV TWILIO_ACCOUNT_SID=your_account_sid
ENV TWILIO_AUTH_TOKEN=your_auth_token
ENV TWILIO_PHONE_NUMBER=your_twilio_phone_number
ENV DESTINATION_PHONE_NUMBER=your_destination_phone_number
ENV WEBSITE=your_website_url

# Run your_script_name.py when the container launches
CMD ["python", "./main.py"]
