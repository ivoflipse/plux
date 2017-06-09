import copy


__all__ = ('Debugger',)


class Debugger:
    """Track changes on a Store on a timeline."""

    def __init__(self, store):
        self._store = store
        
        self.history = [dict(mutation=dict(type=None, payload=None), state=copy.deepcopy(self._store.state)))]
        self.current = 0

        self._store.subscribe(self.on_commit)
    
    def on_commit(self, mutation, state):
        """whenever a mutation is commited to the store we are tracking, make an entry and append it to our history"""
        entry = dict(
            mutation=mutation, 
            state=copy.deepcopy(self._store.state))
        ))
        # this also invalidates all the history that comes after our "current" pointer, in order to support time travel
        self.history = self.history[:self.current+1] + [entry]

    def time_travel(self, index):
        """Time travel to the specified point in history."""
        self._store.state = self.history[index]['state']
        # we update the pointer, so that we may still travel forward in time later on, until someone invalidates that :)
        self.current = index
