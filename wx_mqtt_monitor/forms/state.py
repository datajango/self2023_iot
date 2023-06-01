class State:
    def __init__(self):
        self._state = {}

    def getState(self, key):
        return self._state.get(key)

    def setState(self, key, value):
        self._state[key] = value
