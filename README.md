# How to Schedule a Text Message with Twilio Studio

![Title Image](https://lh3.googleusercontent.com/PjTTCo1HB6VIPBGAUVKr9Nq9ogMsFIABTs84b7DbdcKe-xl3nQUBhVnyhygHKQj8EnyL4BLeLjelnq55CtwpyxrXBaFBSDOzHPapCmF8hUQQJ8Fvxo38dCI0LqBtWS1yTZ_NNVOGgwxYDgds3dylu1o "How to Schedule a Message in Twilio Stuido")

Back in August 2022, we released [Twilio Message Scheduling for general availability](https://www.twilio.com/blog/message-scheduling-is-now-generally-available)! This feature enables you to schedule an SMS, MMS, or WhatsApp message for a fixed time in the future.

Scheduling a message is free of charge and can be done by including the following additional parameters in your API request:

- \`ScheduleType\`: indicates your intent to schedule a message
- \`SendAt\`: indicates when Twilio will send a message

At the time of publishing this blog post, [Twilio Studio](https://www.twilio.com/docs/studio), our low-code/no-code application builder, does not have a built-in feature to schedule messages. In this blog post, you’ll learn a workaround that uses Studio and a bit of Python code.

![](https://lh3.googleusercontent.com/Eny41DRzcKhom_HhMvMb6_9_UslIkPpWRN2WiBgARntlPGmZ5wB_1ShMD3d1KuybOMo9neBCH2FgXPzimaq1YZptyKXuZIMNSbxekDijyQ6apUcMxOs1SuBeCEbLiLTSbB4YGnqVv6yzMkgTrsZqCzw)

> Please note that code snippets will be shown in Python (in this [GitHub repo](https://github.com/anthonyjdella/twilio-schedule-message)), however the same principle applies to [scheduling a message in other languages](https://www.twilio.com/docs/sms/api/message-resource?code-sample=code-create-a-message&code-language=Node.js&code-sdk-version=4.x#schedule-a-message-resource).

This blog post will be structured as followed (feel free to jump ahead):

- **Prerequisites**: Things you need before continuing
- **Step 1**: Create a free Twilio account
- **Step 2**: Buy a Twilio phone number
- **Step 3**: Create a Messaging Service
- **Step 4**: Setup local environment
- **Step 5**: Configure environment variables
- **Step 6**: Schedule a text message with Twilio
- **Step 7**: Create an endpoint to connect with Studio
- **Step 8**: Use Twilio Studio to schedule a message
- **Next Steps & Related Resources**  


## Prerequisites

- [Python 3.7](https://www.python.org/downloads/) or higher installed on your computer
- [ngrok](https://ngrok.com/) installed on your machine. ngrok is a useful tool for connecting your local server to a public URL. You can [sign up for a free account](https://ngrok.com/) and [learn how to install ngrok](https://ngrok.com/download)
- Access to a phone that can make and receive SMS messages


## Step 1: Create a free Twilio account

If you want to give Twilio a spin, and haven’t yet, [sign up for a free Twilio account](https://www.twilio.com/try-twilio). Sign up is quick and no credit card is required!

> The signup process includes [verifying your personal phone number](https://www.twilio.com/docs/usage/tutorials/how-to-use-your-free-trial-account#verify-your-personal-phone-number), as a security measure.


## Step 2: Buy a Twilio phone number

If you haven’t done so already, [buy a Twilio phone number](https://support.twilio.com/hc/en-us/articles/223135247-How-to-Search-for-and-Buy-a-Twilio-Phone-Number-from-Console?_ga=2.241900804.767182747.1677535731-1111941364.1657213658) – a phone number purchased through Twilio – to send messages using Twilio.

After signing up for an account, log in to the [Twilio Console](https://www.twilio.com/console). Then, navigate to the [Phone Numbers](https://console.twilio.com/us1/develop/phone-numbers/manage/active?frameUrl=/console/phone-numbers/incoming&_ga=2.159702331.767182747.1677535731-1111941364.1657213658) page. Click **Buy a Number **to purchase a Twilio number.

![Click Buy a Number to buy a number in Twilio Console](https://lh6.googleusercontent.com/FQ7HeAmw9pg0ZcgMJbWAQhzZ6OsRsDej6LOPcSXn94_Txh1l8hq0NnAVjktSrFqd6Os0XJAA2912TsSQD4sQpFFKyTzHcKEDggpXYBXgKkMOrqk9ApBZ8tngDGKzaiOLIYHK78CHq907s3mjg9HCstc "Buy a Number in Twilio Console")

> When you [sign up for a free Twilio account](https://www.twilio.com/try-twilio), you’re given a [free trial balance](https://support.twilio.com/hc/en-us/articles/223136107-How-does-Twilio-s-Free-Trial-work-) ($15 in the United States) for you to experiment with.

> [Twilio pricing](https://www.twilio.com/en-us/pricing) uses a pay-as-you-go usage-based model for SMS so you aren’t locked into any contracts.



## Step 3: Create a Messaging Service

To take advantage of Message Scheduling, you will need to configure your Twilio number with a [Messaging Service](https://www.twilio.com/docs/messaging/services).

In the [Twilio Console](https://www.twilio.com/console), visit the [Messaging Services page](https://console.twilio.com/?frameUrl=/console/sms/services) and click the **Create Messaging Service** button, then follow the prompts.

![Click Create a Messaging Service to create a messaging service](https://lh3.googleusercontent.com/o3HvDf7I3XSoOTyrv3PTPJzym4xJ3RW2E0b4v6zZOkskL8-TFOSx_ysInXYfYUHaaJ-yyc0x9QmT1uTad5RgaCWRnYDZRd2QON4XKk_hG-z9i_Sf4haKh-2qfMKzjpiydNC2bBXK_f_vniyGhFSPHEQ "Create a Messaging Service")

  


On the next screen, enter a Messaging Service friendly name, such as “schedule-a-message”. Then click the **Create Messaging Service **button.

![For example: schedule-a-message](https://lh4.googleusercontent.com/Fp86owB3Zohw9ejlihE3CBOZpDTCeXojTUHruXQtOn_63KiPMfs2A4mLgW7Ahfdwc_mNfiUrMBrtmu9cWyJ8jm5ZbEB8Vx60uS61OdhiVM6PgopMdNTm57lXR5h_ysgB3mysWhFZ3202u8Yigxjqb9I "Enter a Friendly Name for the Messaging Service")

  


Click the **Add Senders** button to add your Twilio phone number to this Messaging Service.

![Click Add Senders](https://lh4.googleusercontent.com/GN1cHKHfGJl3bHJJsO5BCT3R3BCp2O0ux6Vj749GBYHLtIWHKxSJEqt1naJS2Ax7nOZuMktnKqnCCKH6gKOjzfFJolV64rAoeDrzKOHq0k6d_nlGVy3QeV8LFaXQn7koSzbMBYg2uTqx2HCKo-PKLrM "Add a Sender to the Service")

  


In the **Sender Type** dropdown, select **Phone Number**, then click **Continue**.

![Click continue](https://lh4.googleusercontent.com/OpJ7xkT7cOySbHwl0dCVTH0E_u5u1VjwhJjrO0TTur--h2F-JnqdO6FHGwFIvrbqIWx_Es_FiSsJ_SX76SvLgDCqZqdt1t-k18J-IkUUJzz117Q2HJBGUHrZ8L5Hqzg-S8WXVB36oVSlCkYGdKefxr8 "Add a Sender")

Select your Twilio phone number, by clicking the checkbox next to the number you want to use as a sender. Then click the **Add Phone Numbers** button.

![Select the checkbox](https://lh6.googleusercontent.com/OuSe3RG7SStUulwumEX3EdUAVrvXYZFNHpMdjIzx5kYwkQRhq8MS6HqHPtoysMCM37cVR-f__pEgPbYGPdkOQOv2wD8xHd0ia_tUSMG11tI9mlFEVuZ-YMnGviOQlDyLpkX7LCaIfFhLVKv_jKg9xZ8 "Select your Twilio number")

  


You should see a confirmation notification at the top right corner of the screen that says “Numbers {YOUR-NUMBER} were successfully assigned to the service”

![A successful notification will display on the top right](https://lh6.googleusercontent.com/89B5T7G0Wy9nJnWW_6yz23WXPyVuh4cSGMHCxwIIACE_TV6jInHw9wfZGqf1OTfZo5Z4Q-_EdXpRqOJqczHTzfd-ZOntbmRZoQQG6_dtvY9R2JUd-boyPPVsSNhcZg9S8i3hT2T0pdS1KAaNNJLRZtw "Confirm Notification")

Click the **Step 3: Set up integration** button to continue.

  
  


In this step, you can use the default settings, so click the **Step 4: Add compliance info** button.

![Click continue
](https://lh5.googleusercontent.com/I8oZREKTubllm1GCK552b1nIinVZThAnwNvrMYemh9Snby5oL0UoF0t9mWVEsBd2OvF1WUL9Z2h_Qnz67X6T5X1kUHGvTPXm2tMVcpxz4kSJrpJEDeTeChDr9ddwJyo_fxVidd-NyaRY3_6R0kDD8cQ "Leave Default settings")

  


Next, click the **Complete Messaging Service Setup** button to finalize creating a Messaging Service.

![Continue](https://lh4.googleusercontent.com/7ydDr2nq3InL3VuLdPZZWzSVuNoN8w6D94K76l26-GjFi2o96XYgwdxYVIuMGN_N1EVaW_SronzscwsSOpxzVpGj9vPxYYFXiE5eZo9x4I9WkGvC_giVctcs13uQcCnEy2Uk3JkwXDUnXy2FwkKc958 "Click Continue")

  


To test out your Messaging Service, click the **Try sending a message** button.

![Test the Messaging Service](https://lh5.googleusercontent.com/eJYfJSxA3GyutFlx-k3k0uH_fciQOa97qUmxBsHQn01nnMuHNXdY8-jHvobGFbfn-fYgDYSRi2Rn1Q73BIMu2Mv6rMxNawgJI-ir6YBLE2PDGaa6s-DPeo8TZgVs1_zf2LxkGxxT1AngLOcDUeauRPM "Test the Messaging Service")

  


Continuing on this screen, enter the following details:

- **To phone number,** or the phone number that would receive the message
- In the **From** dropdown, select **Messaging Service**
- Select the Messaging Service which you created earlier
- Input text for the **Body** and click the **Send test SMS** button

![Enter the details to test the service like To, From, Messaging Service, and Body](https://lh6.googleusercontent.com/dm_iEsl-U8a87Vm2CnjU0AXacj_R5T_S7zSTp8uPHqVwu8IDJ1HgPgQWqrj5ZO_3nH9zdsBYJdpo5wqaVYDLM3q68QIJ8pJpeE6Kl4PsoPyCzqnOomZdi8k1UyNOujc7kfr3Df3xHlHaAlrxEPZwhmQ "Enter the details to test the service")

If successful, you should receive an SMS at your test number and see a similar response to the following in the Console:

```
201 - CREATED - The request was successful. We created a new resource and the response body contains the representation.

{

  "body": "Let's test out our Messaging Service!",

  "num_segments": "0",

  "direction": "outbound-api",

  "from": null,

  "date_updated": "Wed, 01 Mar 2023 05:22:27 +0000",

  "price": null,

  "error_message": null,

  "uri": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXX/Messages/SMXXXXXXXXXX.json",

  "account_sid": "ACXXXXXXXXXXXXXXXXX",

  "num_media": "0",

  "to": "+1469XXXXXXX",

  "date_created": "Wed, 01 Mar 2023 05:22:27 +0000",

  "status": "accepted",

  "sid": "SMXXXXXXXXXX",

  "date_sent": null,

  "messaging_service_sid": "MGXXXXXXXXXXXXXXXXX",

  "error_code": null,

  "price_unit": null,

  "api_version": "2010-04-01",

  "subresource_uris": {

    "media": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXX/Messages/SMXXXXXXXXXX/Media.json"

  }

}
```

![Check the message on your phone](https://lh5.googleusercontent.com/m-zAQQ0CWM_sg-fudO32GswVIyIkOGKIi0mSv2wLnDjF6_fMOHxwQeVZiPtdzBfAjdHGi0Po1WxiL5OyEUrn1ARv50o0MVD-kwtdXmEFGs6gwXtYd59kfsq218Y_HNWOV6r3G4z3H5sgseVfZ_-FC1E "Check the message on your phone")

> Once you have created a Messaging Service, you should note down your Messaging Service SID from the [list of Messaging Services](https://www.twilio.com/console/sms/services). It should look similar to this: \`MGXXXXXXXXXXX\`


## Step 4: Setup local environment

Having successfully created a Messaging Service, this step will set up a project that will accommodate your code.

Open a [Terminal window](https://www.youtube.com/watch?v=lZ7Kix9bjPI) and create an empty project directory called _twilio-schedule-message_:

```bash
mkdir twilio-schedule-message
```

Then change into that directory, as that’s where your code will be.

```bash
cd twilio-schedule-message
```

Since the code for this tutorial will be in Python, create a [virtual environment](https://www.twilio.com/docs/usage/tutorials/how-to-set-up-your-python-and-flask-development-environment#start-a-new-project-with-virtualenv):

```bash
python3 -m venv .venv
```

Activate your virtual environment:

```bash
source .venv/bin/activate
```

Then, using the _pip_ package manager, install the required dependencies in your virtual environment:

```bash
pip install python-dotenv twilio>=7.16.5 Flask
```


## Step 5: Configure environment variables

With your local environment set up, it’s time to [configure some environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html) so your credentials are hidden. As a best practice when working with sensitive information like API keys and passwords, it’s important to ensure they are secure and not exposed to the public.

Create a file called _.env_ in the project’s root directory (_twilio-schedule-message/_) to store your API keys.

Within the _.env_ file, create the following environment variables:

```
TWILIO_ACCOUNT_SID=PASTE_YOUR_ACCOUNT_SID_HERE

TWILIO_AUTH_TOKEN=PASTE_YOUR_AUTH_TOKEN_HERE

TWILIO_MSG_SRVC_SID=PASTE_YOUR_MESSAGE_SERVICE_SID_HERE
```

> Make sure to replace \`PASTE_YOUR_ACCOUNT_SID_HERE\` and \`PASTE_YOUR_AUTH_TOKEN_HERE\` with the Account SID and Auth Token associated with your Twilio Account. These can be found on the Homepage of your [Twilio Console](https://console.twilio.com/?_ga=2.137541174.767182747.1677535731-1111941364.1657213658) under **Account Info**.

> Also, replace \`PASTE_YOUR_MESSAGE_SERVICE_SID_HERE\` with the Message Service SID from the Message Service you created earlier. This can be found from the [list of Messaging Services](https://www.twilio.com/console/sms/services).


Your _.env_ file should now look similar to this:

```
TWILIO_ACCOUNT_SID=ACXXXXXXXXXXX

TWILIO_AUTH_TOKEN=12345678901234567

TWILIO_MSG_SRVC_SID=MGXXXXXXXXXXX
```

> If you’re pushing this code to a Git repository, please make sure to add the _.env_ file to your _.gitignore_ so that these credentials are secured. i.e. \`echo ".env" >> .gitignore\`


## Step 6: Schedule a text message with Twilio

In this next step, you will interact with the [Twilio SMS API](https://www.twilio.com/docs/sms/api) to create a scheduled message.

> If you’d like to see the code associated with this blog post, it’s available in this [GitHub repository](https://github.com/anthonyjdella/twilio-schedule-message).

Within your project directory, create a file called _scheduler.py_ and paste the following code into it:

```python
import os

from datetime import datetime

  


from twilio.rest import Client

from twilio.base.exceptions import TwilioRestException

from dotenv import load_dotenv

  


load_dotenv()

  


account_sid = os.getenv('TWILIO_ACCOUNT_SID')

auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)

print(repr(datetime.utcnow()))

  


def schedule_message():

    try:

        message = client.messages \\

            .create(

                messaging_service_sid = os.getenv('TWILIO_MSG_SRVC_SID'),

                to = 'ENTER_THE_NUMBER_YOURE_TEXTING_TO',

                body = 'Ahoy, world! This is a scheduled message in Python.',

                schedule_type = 'fixed',

                send_at = datetime(2023, 3, 3, 5, 55, 10)

            )

        print(message.sid)

    except TwilioRestException as e:

        print(e)

        raise

  


schedule_message()
```

Here’s a breakdown of the code in _scheduler.py_:

- Lines 1-7, are module imports to make use of their functionality.

  - Lines 1-2, provide access to operating system and date functionality.
  - Lines 5-6, provide access to functionality within the Twilio API.
  - Line 7, provides access to environment variables from the _.env_ file.

- Line 10, reads environment variables from the .env file.

- Lines 13-14, assigns variables from the values of your Twilio credentials.

- Line 15, creates a client object using your Twilio credentials.

- Lines 21-34, define a function that sends a scheduled message using the Twilio API.

  - Line 25, \`messaging_service_sid\` parameter is set to the environment variable of your Messaging Service SID, which identifies the Messaging Service used to send the message.
  - Line 26, \`to\` parameter is used as the recipient of the message. Make sure to replace \`ENTER_THE_NUMBER_YOURE_TEXTING_TO\` with the recipient’s number.
  - Line 27, \`body\` parameter sets the text of your message. In this case, the recipient will receive a text message reading, “Ahoy, world! This is a scheduled message in Python.”
  - Line 28, \`schedule_type\` parameter indicates your intent to schedule a message. \`fixed\` means the message is scheduled at a fixed time. 
  - Line 29, \`send_at\` parameter indicates the time that Twilio will send the message. It must be in ISO 8601 format. In this example, the message is scheduled to be sent on March 3, 2023 at 5:55.

- Line 37, invokes the \`schedule_message()\` function and sends out a text message.

To test out the message, run the _scheduler.py _file with this command in your terminal:

```bash
python3 scheduler.py
```

> Message Scheduling supports messages that need to be scheduled more than 15 minutes but fewer than 7 days in advance. Therefore, when modifying the value of the \`send_at\` parameter, make sure it falls within that range (>15 minutes and &lt;7 days).


Your application is now capable of sending a scheduled message at a fixed time in the future. But by modifying the _scheduler.py _file, you can adjust the \`schedule_message()\` function to accept dynamic parameters. This way, instead of hardcoding values into the function, they can be provided at execution time for greater flexibility. Check out changes made to the _scheduler.py _file:

```python

import os

from datetime import datetime

from datetime import timedelta

  


from twilio.rest import Client

from twilio.base.exceptions import TwilioRestException

from dotenv import load_dotenv

  


load_dotenv()

  


account_sid = os.getenv('TWILIO_ACCOUNT_SID')

auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)

  


def schedule_message(minutes, body):

    try:

        message = client.messages \\

            .create(

                messaging_service_sid = os.getenv('TWILIO_MSG_SRVC_SID'),

                to = 'ENTER_THE_NUMBER_YOURE_TEXTING_TO',

                body = body,

                schedule_type = 'fixed',

                send_at = minutes_from_now(minutes)

            )

        print(message.sid)

    except TwilioRestException as e:

        print(e)

        raise

  


def minutes_from_now(minutes):

    if (minutes > 15 and minutes &lt; 10080):

        return datetime.utcnow() + timedelta(minutes=minutes)

    else:

        print('Message must be scheduled more than 15 minutes and fewer than 7 days in advance.')

  


schedule_message(16, 'Ahoy, world! This is another scheduled message in Python.')
```

Here’s a breakdown of the revisions made to _scheduler.py_:

- Line 3, provides access to manipulate date and times.

- Line 20, the \`schedule_message()\` function now accepts two parameters: \`minutes\` and \`body\`. Using the \`minutes\` parameter, you can specify how many minutes in advance you want to schedule a message. Using the \`body\` parameter, you can pass in the body of the text message.

- Line 26, the \`body\` parameter will take in a parameterized message.

- Line 28, the \`send_at\` parameter will invoke a new function called \`minutes_from_now()\` which returns a datetime object.

- Lines 36-40, define a function that returns a datetime object based on the input parameter.

  - Lines 37-38, if the input parameter is within 15 minutes to 7 days in advance, a datetime object will be returned.

- Line 43, invokes the \`schedule_message()\` function and sends out a text message 16 minutes in advance.

Test out the scheduler by re-running the _scheduler.py _file with this command in your terminal:

```bash
python3 scheduler.py
```

Before continuing to the next step, let’s make one more change to our function. Instead of hardcoding a “to” phone number, you can parameterize it. Make note of the following changes to \`schedule_message()\`:

```python

def schedule_message(to_number, minutes, body):

    try:

        message = client.messages \\

            .create(

                messaging_service_sid = os.getenv('TWILIO_MSG_SRVC_SID'),

                to = to_number,

                body = body,

                schedule_type = 'fixed',

                send_at = minutes_from_now(minutes)

            )

        print(message.sid)

    except TwilioRestException as e:

        print(e)

        raise
```

- Line 1, adds a new parameter, \`to_number\`, to the function.
- Line 6, passes the value of \`to_number\` to the \`to\` parameter.
- Delete the call to \`schedule_message()\` at the bottom of the file


## Step 7: Create an endpoint to connect with Studio

In the previous step, you created a function called \`schedule_message()\` that will schedule a message using the Twilio SMS API. In this step, you will create an endpoint using [Flask](https://flask.palletsprojects.com/en/2.2.x/), a web framework for Python. This endpoint will be used later in Studio and interact with the [Make HTTP Request Widget](https://www.twilio.com/docs/studio/widget-library/http-request).

Within your project directory, create a file called _app.py_ and paste the following code into it:

```python

from flask import Flask

from flask import Response

from flask import request

from scheduler import schedule_message

  


app = Flask(\_\_name\_\_)

  


@app.route("/v1/message/schedule", methods=\["POST"])

def send_scheduled_texts():

    try:

        data = request.get_json()

        to_number = data.get("number")

        minutes_ahead = data.get("minutes")

        message = data.get("message")

        schedule_message(to_number, minutes_ahead, message)

        return Response('{"status": "Message sent successfully"}', status=201, mimetype='application/json')

    except Exception as e:

        print(e)

        return Response('{"status": "Message was not sent"}', status=500, mimetype='application/json')

  


app.run(host='localhost', port=3000)

```

Here’s a breakdown of the code in _app.py_:

- Lines 1-3, are module imports to make use of Flask functionality.

- Line 5, is a function import from the previously created _scheduler.py _file.

- Line 8, creates an instance of Flask.

- Lines 11-23, define a function that sets a route for the Flask app to respond to HTTP POST requests via the \`/v1/message/schedule\` endpoint.

  - Lines 13-17, extracts JSON data from the request body and assigns them to variables.
  - Lines 18-20, calls the \`schedule_message()\` function, passing in the data from the JSON request. If the function call succeeds, it returns a Response object with a successful response and a 201 status code.
  - Lines 21-23, if the function call fails, it returns a Response object with a failure response and a 500 status code.

- Line 26, starts the Flask app listening on port 8080 of localhost. 

In a new terminal window, run _app.py_ with the following command:

```bash
python3 app.py
```

> If you receive an error message, you may need to comment out the \`schedule_message()\` invocation in _scheduler.py_ on line 43.

At this point, your server should be running on <http://localhost:8080>. As of now, your application is only running on a server within your computer. But you need a public-facing URL (not <http://localhost>). You could deploy your application to a remote host, but a quick way to temporarily make your web application available on the Internet is by using a tool called [ngrok](https://ngrok.com/product).

In another terminal window run the following command:

```bash
ngrok http 8080
```

This will create a “tunnel” from the public Internet to port 8080 on your local machine, where the Flask app is listening for requests. You should see output similar to this:

![](https://lh4.googleusercontent.com/kiJGa8wChKTJS5XYtuqEZIkGKKHS3i17-vAJW0sH0MGusPvSMfmrPDZgymAtF__YLMfTvODro0IWpTi4Gg894U4HefdTX6jAGFHZZMzzdgFaqLfKmI7UVwH_--Iag9dfeX4yBdAP3YXyyiY6qSI5sBU)

Take note of the line that says “Forwarding”. In the image above, it reads: \`https&#x3A;//5bad813c2718.ngrok.io -> http&#x3A;//localhost:8080\`.

This means that your local application is accessible, publicly, on \`https&#x3A;//5bad813c2718.ngrok.io\` and your endpoint is accessible on \`https&#x3A;//5bad813c2718.ngrok.io/v1/message/schedule\`.

> Each time you run the command \`ngrok http 8080\`, a new Forwarding URL will be randomly generated. 


## Step 8: Use Twilio Studio to schedule a message

Now that you have created the backend for scheduling a message, it’s time to leverage Twilio Studio to schedule a message using your backend application.

You can use an existing Studio Flow or [create a new Flow](https://www.twilio.com/docs/studio/user-guide/get-started#create-a-flow).

To create a new Flow:

1. Navigate to the [Studio Flows section](https://www.twilio.com/console/studio/flows) in the Console.
2. Click the **Create new Flow** button to create a new Flow.
3. Name your Flow. For this project, let’s name it “Schedule SMS in Studio”. Then click **Next**.
4. Select the **Start from scratch** option. Then click **Next**.

From the [Widget Library](https://www.twilio.com/docs/studio/widget-library), drag and drop the **Make HTTP Request** widget onto the Canvas. Then, from the **Trigger** widget, [draw the Transition](https://www.twilio.com/docs/studio/user-guide/get-started#option-1-draw-the-transition-between-two-widgets) from **Incoming Message** to the **Make HTTP Request** widget. Your Flow should look similar to this:

![](https://lh5.googleusercontent.com/-8hyB1nldBzIi65r9C0dYMgWxTJmUHpR5j8wXNBI-P1-TEmNEanPpPoRoW9yMKPVvCjrVLKv2MIEs6x5aGaChAYnaq0x2Z_58UXl_hzirpBtc7E3WGCmPLdng6KXtctxD9Mv2G0VLay9oOSCTpOphiI)

Select the **Make HTTP Request** widget to configure the following properties:

- For the **Widget Name**, call it something like “schedule_message”
- Select “POST” as the **Request Method** in the dropdown
- Set the **Request URL** to “{YOUR-NGROK-URL}/v1/message/schedule” 
- Change the **Content Type** to “Application/JSON” in the dropdown
- Add the following to the **Request Body**:

```json
{

    "number": "{{contact.channel.address}}",

    "minutes": 16,

    "message": "Ahoy, world!"

}
```

> The **Request URL** should point to a [publicly available URL](https://www.twilio.com/docs/usage/webhooks/getting-started-twilio-webhooks#run-your-application-on-a-public-url). If you used ngrok, paste the Forwarding URL from the output of running \`ngrok http 8080\`.

> When modifying _minutes_, make sure it falls within the range (>15 and &lt;10080 minutes), since Message Scheduling supports messages that need to be scheduled more than 15 minutes and fewer than 7 days in advance.

![](https://lh4.googleusercontent.com/4zlUPBSQ4fFbOUldxmV2s9skZDkS53EXWI7SSX3psyYPJt8hDtK6Toq1lHIEsQASyQRVEB0FRtflb_49cuwu6WFepHWVnpQ9MCrQpLUlsonj-ygpZAJUD5R44fTwxUHQZ3IPvp4gUvscwffVcI7_EGE)

Save those changes by clicking the **Save** button. Finally, publish your Flow by clicking the **Publish** button.

![](https://lh4.googleusercontent.com/mz07sSwjPbchRgdeV3AIJOxH8NWe41TqqvL35fF3lHIPBOLdTo_5qK0aoBRej864MFYK3YTE24j-A9Tz10QmnyiKSdekb0bTb-2dUHuDVPkOhrLwYx-Jao1TPaWltsEP8fs2YIVkYwUz53mFj9WEKTA)

Although the Flow is published, you still need to configure your Twilio number to test it out.

Select the **Trigger** Widget by clicking on it. In Flow Configuration, under **Active configurations for this Flow**, click the **Manage Phone Numbers **link.

![](https://lh5.googleusercontent.com/VW3bJeNxN5dvwcjiPDmlkMagzv65CNY9GdOObyppenFBmKKGyAsDa79RL_0B1aOrDMAlWSmUx39GHBGizvV9TzlCiXjfDbKat3qlrh0nE_HPZLmvOOQ0Q4qaBnEBPUW60sFWiZtdshb6XXyCxhkUwmQ)

Select your Twilio phone number and scroll down to the **Messaging** section. Under **A Message Comes In**, select **Studio Flow**. Then select the name of the Studio Flow you created earlier. If you used the example name, it should be “Schedule SMS in Studio”. Then click **Save**.

![](https://lh6.googleusercontent.com/8ERh0Dx3wrZg3THQxIYki4X8qKyeOOtBcq1VOCL0rVJ0Dm08ypQ4jido9T81_zTorb-b0vr0Yyb-eNOp_itvv9y3OfM-f4vEkHJVhKgRN2r2i_H-qMboyGP5ao1hUavXDosEOii18ZKbu4McrNhk7rQ)

With your Flow published, your web server and ngrok running, you can try it out.

> Make sure that your web server and ngrok are running before the message is meant to be scheduled (in this case, 16 minutes).

Since the Flow is triggered by an Incoming Message, send a text message to your Twilio number to trigger the scheduled message.

As a recap, when your Flow is triggered, it makes an HTTP Request to your endpoint \`/v1/message/schedule\`. From there, the \`schedule_message()\` function is called which will send a scheduled message based on the input from Studio.


## Next steps & related resources

Nice job following along, but the fun doesn’t stop here. There are many other features and use cases you can incorporate into your own workflows. For instance, you can see a [list of scheduled messages](https://www.twilio.com/console/sms/logs) and also [cancel a scheduled message](https://www.twilio.com/docs/sms/api/message-resource#cancel-a-scheduled-message) before it’s sent.

For more information about scheduling a message and answering common questions, see the [Message Scheduling FAQs](https://support.twilio.com/hc/en-us/articles/4412165297947-Message-Scheduling-FAQs-and-Limitations).

If you’d like to see the code associated with this blog post, it’s available in this [GitHub repository](https://github.com/anthonyjdella/twilio-schedule-message).

Thanks so much for reading! If you found this tutorial helpful, have any questions, or want to show me what you’ve built, let me know online. And if you want to learn more about me, check out [my intro blog post](https://www.twilio.com/blog/introducing-twilio-developer-evangelist-anthony-dellavecchia).

![](https://lh5.googleusercontent.com/QqqYPg-hhp8oQKv4XEWLDNhjs5DrmgJbm_qEWZWJLzudWG9T46R7OIGWhVDRHjosLv7aM-I3xXxzORP6VhiUjbJvZIjiO1RZx-aLdIJXwZUMXTgwR8b1FRzWKra4KTQP2gljGhKXRG1fp83uWqkYbEk)

> _Anthony Dellavecchia is a Developer Evangelist at Twilio who writes code on stage in front of a crowd. He is an experienced software developer who teaches thousands of people how to change the world with code. His goal is to help you build deep experiences and connections with technology so that they stick with you forever._

> _Check him out online @anthonyjdella -- _[_Twitter_](https://twitter.com/anthonyjdella)_ • _[_Linkedin_](https://www.linkedin.com/in/anthonydellavecchia/)_ • _[_GitHub_](https://github.com/anthonyjdella)_ • _[_TikTok_](https://tiktok.com/@anthonyjdella)_ • _[_Medium_](https://medium.com/@anthonyjdella)_ • _[_Dev.to_](https://dev.to/anthonyjdella)_ • Email • _[_anthonydellavecchia.com_](https://anthonydellavecchia.com/)_ 👈_
