
def generate_diageo_time_table():    
    lines = [
    '  7 | Nights before weekdays  | 20:00:00      | 23:59:59    | f      | f      | f       | f         | t        | f      | f',
    ' 12 | Nights before weekends  | 20:00:00      | 23:59:59    | f      | f      | f       | f         | f        | t      | t',
    ' 13 | Weekends after midnight | 00:00:00      | 02:00:00    | t      | f      | f       | f         | f        | f      | t',
    ' 16 | Saturday lunch          | 12:00:00      | 13:00:00    | f      | f      | f       | f         | f        | f      | t',
    ' 21 | Friday/Saturday dinner  | 19:00:00      | 20:00:00    | f      | f      | f       | f         | f        | t      | t',
    ' 22 | Sunday-Thursday dinner  | 19:00:00      | 20:00:00    | f      | f      | f       | f         | t        | f      | f',
    ' 23 | Weekday overnight       | 00:00:00      | 06:00:00    | f      | f      | f       | f         | f        | t      | f',
    ' 17 | Saturday afternoon      | 13:00:00      | 17:00:00    | f      | f      | f       | f         | f        | f      | t',
    '  9 | PM business hours       | 13:00:00      | 16:00:00    | f      | f      | f       | f         | t        | t      | f',
    ' 11 | PM commute              | 17:30:00      | 18:30:00    | f      | f      | f       | f         | t        | t      | f',
    ' 28 | Saturday late afternoon | 17:00:01      | 18:59:59    | f      | f      | f       | f         | f        | f      | t',
    ' 31 | Late PM business hours  | 16:00:01      | 17:29:59    | f      | f      | f       | f         | t        | t      | f',
    ' 32 | Weekday early evening   | 18:30:01      | 18:59:59    | f      | f      | f       | f         | t        | t      | f'
    ]
    for line in lines:
        # remove all whitespace
        clean_string = ''.join(line.split())
        tp, desc, begin, end, sunday, monday, tuesday, wednesday, thursday, friday, saturday = clean_string.split('|')
        begin_hour, begin_min, begin_sec = begin.split(':')
        end_hour, end_min, end_sec = end.split(':')
        begin_secs  = int(begin_sec) + 60 * ( int(begin_min) + 60 * int(begin_hour) )
        end_secs    = int(end_sec)   + 60 * ( int(end_min)   + 60 * int(end_hour) )
        truth_line = 'elif secs >= ' + str(begin_secs) + ' and secs <= ' + str(end_secs) + ' and day in [ '
        if monday == 't':       truth_line += '0,'
        if tuesday == 't':    truth_line += '1,'
        if wednesday == 't':  truth_line += '2,'
        if thursday == 't':   truth_line += '3,'
        if friday == 't':     truth_line += '4,'
        if saturday == 't':   truth_line += '5,'
        if sunday == 't':     truth_line += '6,'
        truth_line = truth_line[:-1]
        truth_line += '] : return ' + tp
        print truth_line

generate_diageo_time_table()