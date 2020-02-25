# Robo-Advisor Project

## Basic Requirements

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

### API Requirements and Security

You will need a personalized API Key to issue requests to the [AlphaVantage API](https://www.alphavantage.co) so that the program can retrieve stock data. But the program's source code will not include the secret API Key value. Instead, you should include your API Key in a variable called `ALPHAVANTAGE_API_KEY` in the .env directory, and the program will read the API Key from this environment variable at run-time. 

Since .env files will be included in the .gitignore directory, your API key will be kept secret.

### Twilio Setup

For SMS capabilities, [sign up for a Twilio account](https://www.twilio.com/try-twilio), click the link in a confirmation email to verify your account, then confirm a code sent to your phone to enable 2FA.

Then [create a new project](https://www.twilio.com/console/projects/create) with "Programmable SMS" capabilities. And from the console, view that project's Account SID and Auth Token. Update the contents of the ".env" file to specify these values in the exisiting `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`, respectively.

You'll also need to [obtain a Twilio phone number](https://www.twilio.com/console/sms/getting-started/build) to send the messages from. After doing so, update the contents of the ".env" file to specify this value (including the plus sign at the beginning) in the environment variable called `SENDER_SMS`.

Finally, specify the recipient's phone number in the environment variable called `RECIPIENT_SMS` to specify the recipient's phone number (including the plus sign at the beginning).