import datetime
import math

import utils
import constants

# TLE variables for ISS. TODO: Import from raw.
epoch = "19209.53234192"
inclination = 51.6398 # degrees
raan = 156.1486 # degrees
eccentricity = 0.0006337
arg_of_perigee = 192.2040 # degrees
mean_anomaly = 167.8958 #degrees
mean_motion = 15.50992959 #rev/day
decay_rate = 1.6717e-4 # rev/day^2

# Derived variables
utcEpoch = utils.datetime_from_epoch(epoch)
inclination_rad = math.radians(inclination)
raan_rad = math.radians(raan)
arg_of_perigee_rad = math.radians(arg_of_perigee)
mean_anomaly_rad = math.radians(mean_anomaly)
mean_motion_rps = mean_motion * (2 * math.pi) / 86400
decay_rate_rps2 = decay_rate * (2 * math.pi) / 86400**2

period_seconds = (2 * math.pi) / mean_motion_rps
semi_major_meters = ((constants.G*constants.M*period_seconds) / (4 * math.pi**2))**(1.0/3.0)
semi_minor_meters = semi_major_meters * math.sqrt(1 - eccentricity**2)
print("Semi-Major Axis: %f meters" % semi_major_meters)
print("Semi-Minor Axis: %f meters" % semi_minor_meters)


# Inputs
time_to_predict = datetime.datetime.utcnow()

# Let's get started
print("Epoch: %s" % utcEpoch)
print("Predict At: %s" % time_to_predict)

# Propagate the mean anomaly
# time since epoch
delta_T = time_to_predict - utcEpoch
delta_T_seconds = delta_T.total_seconds()


# Find new mean anomaly
M = (mean_anomaly_rad + (mean_motion_rps * delta_T_seconds) - (0.5 * decay_rate_rps2 * delta_T_seconds**2)) % (2 * math.pi)

# Solve Kepler's equation using Newton's method
# E is the eccentric anomaly
E = M
while True:
	delta_E = (E - eccentricity * math.sin(E) - M) / (1 - eccentricity * math.cos(E))
	E -= delta_E
	if math.fabs(delta_E) < 1e-9:
		break


# Given E, find coordinates in orbital plane (P, Q)
P = semi_major_meters * (math.cos(E) - eccentricity)
Q = semi_minor_meters * math.sin(E)

## ROTATION into siderial frame
x = (math.cos(arg_of_perigee_rad) * math.cos(raan_rad) - math.sin(arg_of_perigee_rad) * math.sin(raan_rad) * math.cos(inclination_rad)) * P + \
	(-math.sin(arg_of_perigee_rad) * math.cos(raan_rad) - math.cos(arg_of_perigee_rad) * math.sin(raan_rad) * math.cos(inclination_rad)) * Q

y = (math.cos(arg_of_perigee_rad) * math.sin(raan_rad) + math.sin(arg_of_perigee_rad) * math.cos(raan_rad) * math.cos(inclination_rad)) * P + \
	(-math.sin(arg_of_perigee_rad) * math.sin(raan_rad) + math.cos(arg_of_perigee_rad) * math.cos(raan_rad) * math.cos(inclination_rad)) * Q

z = (math.sin(arg_of_perigee_rad) * math.sin(inclination_rad)) * P + (math.cos(arg_of_perigee_rad) * math.sin(inclination_rad)) * Q


print ("(%f, %f, %f)" % (x, y, z))

## PROJECT to lat, lng
# Convert to spherical
r = math.sqrt(x**2 + y**2 + z**2)
ra_rad = math.atan2(y, x)
dec_rad = math.acos(z / r)

gmst_rad = utils.greenwich_siderial_time(time_to_predict) * (2 * math.pi / 24)

lng_rad = -gmst_rad + ra_rad
lat_rad = (math.pi / 2) - dec_rad
if lng_rad > math.pi:
	lng_rad = lng_rad - 2 * math.pi
elif lng_rad < -math.pi:
	lng_rad = lng_rad + 2 * math.pi

lng = math.degrees(lng_rad)
lat = math.degrees(lat_rad)

print("Latitude: %f degrees" % lat)
print("Longitude: %f degrees" % lng)

