class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, action):
        if action == 1:
            self.x += 1
        elif action == 2:
            self.x -= 1
        elif action == 3:
            self.y += 1
        elif action == 4:
            self.y -= 1
        return self.x, self.y