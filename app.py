from flask import Flask, jsonify, request

app = Flask(__name__)


class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    new_id = max((e.id for e in events), default = 0) + 1
    event = Event(id=new_id, title=data["title"])
    events.append(event)
    return jsonify(event.to_dict()), 201


@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()
    event = next((e.to_dict() for e in events if e.id == event_id), None)
    if not event:
        return("Event not found!", 404)
    if "title" in data:
        event["title"] = data["title"]
    return jsonify(event), 200


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    global events
    event = next((e for e in events if e.id == event_id), None)
    if not event:
        return("Event not found", 404)
    events = [e for e in events if e.id != event_id]
    return("Event deleted successfully", 204)

if __name__ == "__main__":
    app.run(debug=True)
