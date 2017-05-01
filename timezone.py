import pytz
import datetime


amsterdam = pytz.timezone('Pacific/Auckland')

datetime_without_tz = datetime.datetime.strptime("Mon May 01 20:00:00 +0000 2017", "%a %b %d %H:%M:%S %z %Y")

datetime_in_au = datetime_without_tz.astimezone(amsterdam)
 
str1 = datetime_without_tz.strftime('%Y-%m-%d %H:%M:%S %Z')
str3 = datetime_in_au.strftime('%Y-%m-%d %H:%M:%S %Z')
 
print ('Without Timzone : %s' % (str1))
print ('AUCKLAND Datetime    : %s' % (str3))

