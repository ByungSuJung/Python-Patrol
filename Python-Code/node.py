class Node:
    def __init__(self,id,x,y,cap):
        import Queue as Q
        import constants as c
        self.id = id
        self.x = x
        self.y = y
        self.cap = cap
        self.time_steps = c.NODE_TIME_STEPS
        self.q = Q.Queue(maxsize=self.cap)
        self.q_size = 0
