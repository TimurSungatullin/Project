from FlyingObjects import FlyingObjects


class Asteroid(FlyingObjects):
    def __init__(self, cX, cY):
        FlyingObjects.__init__(self, "asteroid.png", cX, cY)