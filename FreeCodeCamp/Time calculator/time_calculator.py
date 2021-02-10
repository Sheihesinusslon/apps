def add_time(start: str, duration: str, weekday=None) -> str:
  '''
  function takes initial time 'start' and duration time 'duration' and returns the final time in clock format; if it's not the same day, shows how many days passed; if given optional parameter 'weekday', figures out and shows the final weekday
  '''
  # decompose inputs on hours and minutes
  st = start.split()
  st_time, day  = st[0], st[1] # day = AM or PM
  div = st_time.find(':')
  st_hours = st_time[:div]
  st_mins = st_time[div+1:]
  dur = duration.split(':')
  dur_hours, dur_mins = dur[0], dur[1]

  # calculate primary result and set default
  # time of the day and days passed
  res_hours = int(st_hours) + int(dur_hours)
  res_mins = int(st_mins) + int(dur_mins)
  res_day = day
  days_passed = 0
  
  # normilize minutes to clock format
  if res_mins > 59:
    res_hours += res_mins//60
    res_mins -= (res_mins//60)*60
  if res_mins < 10:
    res_mins = '0' + str(res_mins)

  # figure out time of the day
  if res_hours > 11:
    if day=='AM': res_day = day if (res_hours//12)%2==0 else 'PM'
    else: res_day = day if (res_hours//12)%2==0 else 'AM'
    
    # figure out actual days passed
    days_passed = (res_hours//24)+1 if day=='PM' else res_hours//24

    # normilize hours to clock format
    res_hours -= (res_hours//12)*12
    if res_hours == 0: res_hours = 12
  
  # prepare primary result in string format
  result = f'{str(res_hours)}:{str(res_mins)} {res_day}'

  # if given optional parameter 'weekday'
  # figure out what weekday to display based on days passed
  if weekday:
    weekday = weekday.lower()
    if not days_passed:
      result += ', ' + weekday.capitalize()
    else:
      weekday_list = ['monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday', 'sunday']
      # simple algorythm to get the correct weekday
      index = weekday_list.index(weekday)
      counter = days_passed
      while counter:
        index += 1
        if index > 6:
          index = 0
        counter -= 1
      
      # add weekday parameter to the final result
      weekday = weekday_list[index]
      result += ', ' + weekday.capitalize()
 
  # add how many days passed to the final result
  if days_passed:
    if days_passed==1: result += ' (next day)'
    else: result += f' ({str(days_passed)} days later)'

  return result