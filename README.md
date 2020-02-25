# Robo-Advisor Project
### Environment Setup

Create and activate a new Anaconda virtual environment:

```sh
conda create -n stocks-env python=3.7 (first time only)
conda activate stocks-env
```

From within the virtual environment, install the required packages specified in the "requirements.txt" file:

```sh
pip install -r requirements.txt
```

Twilio Setup...

For SMS capabilities, sign up for a Twilio account, click the link in a confirmation email to verify your account, then confirm a code sent to your phone to enable 2FA.

Then create a new project with "Programmable SMS" capabilities. And from the console, view that project's Account SID and Auth Token. Update the contents of the ".env" file to specify these values as environment variables called TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN, respectively.

You'll also need to obtain a Twilio phone number to send the messages from. After doing so, update the contents of the ".env" file to specify this value (including the plus sign at the beginning) as an environment variable called SENDER_SMS.

Finally, set an environment variable called RECIPIENT_SMS to specify the recipient's phone number (including the plus sign at the beginning).

Usage...
