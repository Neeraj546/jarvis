from datetime import date, datetime
import calendar
today = date.today()
now = datetime.now()
hours = int(now.strftime("%H"))
mins = int(now.strftime("%M"))
todaydat = int(today.strftime("%d"))
todaymon = today.strftime("%B")
todayyear = int(today.strftime("%Y"))
todayday = calendar.day_name[today.weekday()]
