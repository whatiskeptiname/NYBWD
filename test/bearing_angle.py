import math

def angleFromCoordinate(lat1, long1, lat2, long2):
    dLon = (long2 - long1)
    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
    brng = math.atan2(y, x)
    brng = math.degrees(brng)
    brng = (brng + 360) % 360
    brng = 360 - brng # count degrees clockwise - remove to make counter-clockwise
    return brng


val = angleFromCoordinate(27.698456082179106, 85.29502805133828, 27.69847569688809, 85.29702034811457)
print(val)

def rotation(bposn, bdest):
    brotation = bdest - bposn
    if brotation< -180: 
        brotation = brotation + 360
    if brotation > 180:
        brotation = brotation - 360

    print(brotation)

rotation(0, 270)


def turn(self, turnangle, speed):
        if turnangle > 0 :
            bposn = self.positionBearing()
            new_bearing = (bposn + turnangle) % 360
            while True:
                self.right(speed)
                bposn = self.positionBearing()
                print(bposn)
                if bposn == None:
                    self.stop()
                    continue
                if bposn >= new_bearing:
                    self.stop()
                    break

        if turnangle < 0 :
            bposn = self.positionBearing()
            new_bearing = (bposn + turnangle)
            while True:
                self.left(speed)
                bposn = self.positionBearing()
                print(bposn)
                if bposn == None:
                    self.stop()
                    continue
                if bposn <= new_bearing:
                    self.stop()
                    break