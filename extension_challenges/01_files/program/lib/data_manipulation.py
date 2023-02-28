import os
#/Users/phoebeswaine/Projects/python_foundations/extension_challenges/01_files/program/AirQuality.csv

# == INSTRUCTIONS ==
#
# Below, you'll find lots of incomplete functions.
#
# Your job: Implement each function so that it does its job effectively.
#
# Tips:
# * Use the material, Python Docs and Google as much as you want
#
# * A warning: the data you are using may not contain quite what you expect;
#   cleaning data (or changing your program) might be necessary to cope with
#   "imperfect" data

# == EXERCISES ==

# Purpose: return a boolean, False if the file doesn't exist, True if it does
# Example:
#   Call:    does_file_exist("nonsense")
#   Returns: False
#   Call:    does_file_exist("AirQuality.csv")
#   Returns: True
# Notes:
# * Use the already imported "os" module to check whether a given filename exists
def does_file_exist(filename):
    if os.path.exists(filename):
        return True
    else:
        return False


# Purpose: get the contents of a given file and return them; if the file cannot be
# found, return a nice error message instead
# Example:
#   Call: get_file_contents("AirQuality.csv")
#   Returns:
#     Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);[...]
#     10/03/2004;18.00.00;2,6;1360;150;11,9;1046;166;1056;113;1692;1268;[...]
#     [...]
#   Call: get_file_contents("nonsense")
#   Returns: "This file cannot be found!"
# Notes:
# * Learn how to open file as read-only
# * Learn how to close files you have opened
# * Use readlines() to read the contents
# * Use should use does_file_exist()
def get_file_contents(filename):
    if does_file_exist(filename):
        with open(filename, 'r') as f:
            contents = f.readlines()
        return contents
    else:
        return "This file cannot be found!"


# Purpose: fetch Christmas Day (25th December) air quality data rows, and if
# boolean argument "include_header_row" is True, return the first header row
# from the filename as well (if it is False, omit that row)
# Example:
#   Call: christmas_day_air_quality("AirQuality.csv", True)
#   Returns:
#     Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);[...]
#     25/12/2004;00.00.00;5,9;1505;-200;15,6;1168;567;525;169;1447;[...]
#     [...]
#   Call: christmas_day_air_quality("AirQuality.csv", False)
#   Returns:
#     25/12/2004;00.00.00;5,9;1505;-200;15,6;1168;567;525;169;1447;[...]
#     [...]
# Notes:
# * should use get_file_contents() - N.B. as should any subsequent
# functions you write, using anything previously built if and where necessary
def christmas_day_air_quality(filename, include_header_row):
    contents = get_file_contents(filename)
    output = []
    if include_header_row:
        output.append(contents[0][:4])
    # If the date is equal the the 25/12 then append it and return it
    for line in contents:
        if line[:5] == '25/12':
            output.append(line)
    return output

# Purpose: fetch Christmas Day average of "PT08.S1(CO)" values to 2 decimal places
# Example:
#   Call: christmas_day_average_air_quality("AirQuality.csv")
#   Returns: 1439.21
# Data sample:
# Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);NOx(GT);PT08.S3(NOx);NO2(GT);PT08.S4(NO2);PT08.S5(O3);T;RH;AH;;
# 10/03/2004;18.00.00;2,6;1360;150;11,9;1046;166;1056;113;1692;1268;13,6;48,9;0,7578;;
def christmas_day_average_air_quality(filename):
    christmas = christmas_day_air_quality(filename, False)
    average = 0
    sum = 0
    count = 0
    for record in christmas:
        # Splits the contents by converting ';' to breaks
        record = record.split(';')
        # Sums the '3rd' column and counts the amount of times it has been ran through
        sum += int(record[3])
        count += 1
    # calculates the average, rounds it to 2 decimnal places and then returns
    average = sum/count
    average = round(average, 2)
    return average

# Purpose: scrape all the data and calculate average values for each of the 12 months
#          for the "PT08.S1(CO)" values, returning a dictionary of keys as integer
#          representations of months and values as the averages (to 2 decimal places)
# Example:
#   Call: get_averages_for_month("AirQuality.csv")
#   Returns: {1: 1003.47, [...], 12: 948.71}
# Notes:
# * Data from months across multiple years should all be averaged together
def get_averages_for_month(filename):
    contents = get_file_contents(filename)
    # Pops off the 'header' line
    contents.pop(0)
    # All variables 
    data = 0
    _month = 3
    counts = {}
    months = {}
    average = 0
    count = 0
    sum = 0
    # As the code is turning lists of string into integers empty strings canot be onverted an therefor are ignored in this
    for record in contents[:-114]:
        record = record.split(';')
        # From the .csv we are capturing the date, splitting it into three sections with .split('/') colecting the month as it is the second in the list [1]
        # and then converting it into a integer
        month = int(record[0].split('/')[1])
        data = int(record[3])
        if month != _month:
            average = sum/count
            average = round(average, 2)
            # prints all data collected for each month
            print (f"Sum: {sum}, count: {count}, month: {_month}, average: {average}")
            # No has.hash in python 3.9 but looks for duplicate 'keys'
            if _month in months:
                # Since there are two 'keys' within this dictionary we need to find out the average between the two
                # As the 2nd 'keys' data hasn't been stored within the dictionary yet but rather inside 'sum' we can
                # caculate the new average by using the old average, sum, count and _months
                old_average = months[_month]
                old_average = old_average * (counts[_month])
                new_average = old_average + sum
                n = count + counts[_month]
                new_average = new_average / n
                new_average = round(new_average, 2)
                months[_month] = new_average
            else:
                months[_month] = average
                counts[_month] = count
            # Refreshes the data for the next month
            sum = 0
            count = 0
            _month = month
        sum += data
        count += 1
    return months

# Purpose: write only the rows relating to March (any year) to a new file, in the same
# location as the original, including the header row of labels
# Example
#   Call: create_march_data("AirQuality.csv")
#   Returns: nothing, but writes header + March data to file called
#            "AirQualityMarch.csv" in same directory as "AirQuality.csv"
def create_march_data(filename):
    contents = get_file_contents(filename)
    output = [contents.pop(0)]
    for record in contents[:-114]:
        _record = record.split(';')
        month = int(_record[0].split('/')[1])
        if month == 3:
            output += record
    output = ''.join(output)
    with open('AirQualityMarch.csv', 'w') as f:
        f.write(output)


# Purpose: write monthly responses files to a new directory called "monthly_responses",
# in the same location as AirQuality.csv, each using the name format "mm-yyyy.csv",
# including the header row of labels in each one.
# Example
#   Call: create_monthly_responses("AirQuality.csv")
#   Returns: nothing, but files such as monthly_responses/05-2004.csv exist containing
#            data matching responses from that month and year
def create_monthly_responses(filename):
    # Makes directory
    os.makedirs('monthly_responses', exist_ok=True)
    # For each month 
    data1 = [[] for i in range (12)]
    data2 = [[] for i in range (12)]
    # Make file
    contents = get_file_contents(filename)
    header = contents.pop(0)
    # Name file properly
    for record in contents[:-114]:
        _record = record.split(';')
        date = _record[0].split('/')
        month = int(date[1])
        year = int(date[2])
        _month = date[1]
        _year = date[2]
        if year == 2004:
            # gather months and put in data 1
            data1[month-1].append(record)
        elif year == 2005:
            # gather months and put in data 2
            data2[month-1].append(record)
    # Dump data in file
    for month in data1 + data2:
        if len(month) == 0:
            continue
        else:
            # Fetch date from records from colletion of records
            _date = month[0].split(';')[0].split('/')
            month .insert(0, header)
            month = ''.join(month)
            with open(f'monthly_responses/{_date[1]}-{_date[2]}.csv', 'w') as f:
                f.write(month)


    # Give header
    # Give Data
    # next file
    # return nothing



create_monthly_responses('AirQuality.csv')