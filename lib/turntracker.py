class TurnTracker:
    time_delta = 60
    def __init__(self):
        self.headings = []
    
    def track(self, angle):
        self.headings.append(angle)
        if len(self.headings) > TurnTracker.time_delta:
            self.headings.pop(0)
    
    def get_angle(self):
        if len(self.headings) == 0:
            return 0
        if len(self.headings) < TurnTracker.time_delta:
            return (self.headings[-1] - self.headings[0]) 
        return (self.headings[-1] - self.headings[-TurnTracker.time_delta]) 
