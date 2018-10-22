from FlyingObjects import FlyingObjects


class Spaceship(FlyingObjects):
    def __init__(self, cX, cY):
        FlyingObjects.__init__(self, "shuttle.png", cX, cY)
