from flask import Flask, abort
from flask_restful import Api, Resource, inputs, reqparse, fields, marshal_with
from datetime import date
import sys
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)


db.create_all()

post_parser = reqparse.RequestParser()
get_parser = reqparse.RequestParser()

get_parser.add_argument(
    'start_time',
    type=str,
    help='',
    required=False
)
get_parser.add_argument(
    'end_time',
    type=str,
    help='',
    required=False
)
post_parser.add_argument(
    'event',
    type=str,
    help='The event name is required!',
    required=True
)
post_parser.add_argument(
    'date',
    type=inputs.date,
    help='The event date with the correct format is required! The correct format is YYYY-MM-DD!',
    required=True
)


resource_fields = {
    'id': fields.Integer,
    'event': fields.String,
    'date': fields.DateTime(dt_format='iso8601')
}


class EventByIdResource(Resource):
    @marshal_with(resource_fields)
    def get(self, event_id, **kwargs):
        event = Event.query.filter_by(id=event_id).first()
        if not event:
            abort(404, "The event doesn't exist!")
        return event

    def delete(self, event_id, **kwargs):
        event = Event.query.filter_by(id=event_id).first()
        if not event:
            abort(404, "The event doesn't exist!")
        db.session.delete(event)
        db.session.commit()
        return {"message": "The event has been deleted!"}


class TodayEventsResource(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        events = Event.query.filter_by(date=date.today()).all()
        return events


class AddEventResource(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        args = get_parser.parse_args()
        start_time = args['start_time']
        end_time = args['end_time']
        if start_time and end_time :
            events = Event.query.filter(Event.date.between(start_time, end_time)).all()
        else:
            events = Event.query.all()
        return events

    def post(self):
        args = post_parser.parse_args()
        event = Event(event=args['event'], date=args['date'].date())
        db.session.add(event)
        db.session.commit()

        return {
            'message': 'The event has been added!',
            'event': args['event'],
            'date': str(args['date'].date())
        }


api.add_resource(TodayEventsResource, '/event/today')
api.add_resource(AddEventResource, '/event')
api.add_resource(EventByIdResource, '/event/<int:event_id>')

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
