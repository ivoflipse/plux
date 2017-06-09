class Store:
    def __init__(self, state, mutations, actions):
        """
        Parameters
        ----------
        state : any
            The root state object.
        mutations : dict
            Mapping of mutation types to handlers. The function receives state and payload as arguments.
        actions : dict
            Mapping of action types to handlers. The function receives state, commit, dispatch as arguments.
        """
        self.state = state
        self._mutations = mutations
        self._actions = actions
        self._subscribers = []

    def commit(self, type, payload=None):
        """commit a mutation"""
        self._mutations[type](self.state, payload=payload)
        
        # notify our subscribers of the change
        for sub in self._subscribers:
            sub(dict(type=type, payload=payload), self.state)

    def dispatch(self, type, payload=None):
        """dispatch an action"""
        self._actions[type](self.state, payload=payload)

    def subscribe(self, handler):
        """
        register a handler to be called when a mutation is committed. the handler is passed the mutation 
        type, payload and the post-mutation state.
        """
        self._subscribers.append(handler)
