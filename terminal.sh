docker build -t websiteupdatenotification .
docker run -d --restart always \
           -e TEST_PROGRAM=False \
           -e TWILIO_ACCOUNT_SID=your_account_sid \
           -e TWILIO_AUTH_TOKEN=your_auth_token \
           -e TWILIO_PHONE_NUMBER=your_twilio_phone_number \
           -e DESTINATION_PHONE_NUMBER=your_destination_phone_number \
           -e WEBSITE=https://example.com \
           websiteupdatenotification