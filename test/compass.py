import py_qmc5883l
sensor = py_qmc5883l.QMC5883L()
m = sensor.get_magnet()
print(sensor.get_bearing())