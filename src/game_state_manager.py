class GameStateManager:
    def __init__(self, renderer, data_manager):
        self.renderer = renderer
        self.dm = data_manager
        self.states = {}
        self.current_state_name = None
        self.current_state = None

    def register_state(self, name, state_instance):
        self.states[name] = state_instance
        state_instance.manager = self

    def change_state(self, name, **kwargs):
        if name in self.states:
            if self.current_state:
                self.current_state.exit()
            self.current_state_name = name
            self.current_state = self.states[name]
            self.current_state.enter(**kwargs)
        else:
            print(f"State {name} not found!")

    def update(self, dt, events):
        if self.current_state:
            self.current_state.update(dt, events)

    def draw(self):
        if self.current_state:
            self.current_state.draw()
