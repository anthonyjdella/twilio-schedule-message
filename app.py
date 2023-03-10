from flask import Flask
from flask import Response
from flask import request

from scheduler import schedule_message


app = Flask(__name__)


@app.route("/v1/message/schedule", methods=["POST"])
def send_scheduled_texts():
    data = request.get_json()
    to_number = data.get("number")
    minutes_ahead = data.get("minutes")
    message = data.get("message")

    try:
        schedule_message(to_number, minutes_ahead, message)
        return Response('{"status": "Message sent successfully"}', status=201, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response('{"status": "Message was not sent"}', status=500, mimetype='application/json')


if __name__ == "__main__":
    app.run(host='localhost', port=3000)
