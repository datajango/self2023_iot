class Event:
    def __init__(self):
        self._events = {}

    def register(self, event_name, function):
        self._events[event_name] = function

    def trigger(self, event_name, *args, **kwargs):
        if event_name in self._events:
            return self._events[event_name](*args, **kwargs)
        else:
            raise Exception(f"No event named {event_name}")
