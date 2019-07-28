import datetime

def datetime_from_epoch(epoch):
	(date_part, fractional_part) = epoch.split(".")
	fractional_part = "0.%s" % fractional_part
	date = datetime.datetime.strptime(date_part, "%y%j")
	date += datetime.timedelta(
		seconds=86400*float(fractional_part))

	return date


def julian_date(time):
	UT = (time.minute / 60.0) + time.hour
	JD = (367*time.year) - \
	int((7*(time.year+int((time.month+9)/12)))/4) + \
	int((275*time.month)/9) + time.day + 1721013.5 + (UT/24)
	return JD

def greenwich_siderial_time(time):
	GMST = 18.697374558 + 24.06570982441908*(julian_date(time) - 2451545)
	return GMST % 24
	