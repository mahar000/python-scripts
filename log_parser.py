#!/usr/bin/env python3
'''
Script to parse smf log files , script is using config file in csv format,
the config file is  mystrings.csv
file format is
string1,string2,string3

script will generate grep  as follows
grep -E 'string1' RTC.csv|grep -E  'string2'|grep -E 'string3'
Sample  grep string file

cat mystrings_rtc.csv
grep -E  'ERROR:|CRITITCAL:|WARNING:',|grep -v 'Unexpected answer received',
grep -E  'established',
grep -E 'changed: OPEN',
grep -Ei  'Exception',
grep -E  'WARNING: Gx Server Overload',
grep -E OVERLOAD,
grep -E "Broken pipe",
grep -E  broken,


'''

from datetime import datetime, timedelta
import subprocess
import csv


def get_log():
    '''
    Function to get last 5 minutes log
    '''
    now = datetime.now()
    print(now)
    lookback = timedelta(minutes=5)
    print(lookback)
    five_min_before = (now - lookback).strftime("%b %e %H:%M:%S")
    # five_min_before = (now - lookback).strftime("%m/%d/%Y %H:%M:%S")
    print(five_min_before)
    with open(result_file, 'w') as file_object:
        with open(File, 'r') as f:
            for line in f:
                try:
                    mytime = datetime.strptime(line[0:19], '%b %e %H:%M:%S')
                    if mytime < five_min_before:
                        continue
                    elif mytime > five_min_before:
                        file_object.write(line.strip())
                except ValueError:
                    continue


def get_files():
    '''
    This function is not used yet, we can use it in the Future,
    if we need to generate any stats using pandas
    '''
    subprocess.call("awk -F: '{print NF}' RTC.csv |sort -nu|\
    while read line;\
    do awk -F: '(NF=='$line') {print }' RTC.csv  >RTC_${line}.csv;done ",
                    shell=True)

    cmd = "ls RTC_*.csv"
    output = subprocess.run(cmd, shell=1, stdout=subprocess.PIPE).stdout.decode('utf-8')

    file_list = output.split()
    print(file_list)


def get_results():
    '''
    function to  get the grep command
    '''

    with open(final_result, "a+") as f1:
        with open(string_file, "r", encoding="utf-8") as  csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                myarray1 = row
                myarray = list(filter(None, myarray1))
                # print(myarray)

                if len(myarray) == 1:
                    str = f"{myarray[0]} {result_file} "
                    print(str)
                    cmd = str
                    subprocess.run([cmd], shell=True, stdout=f1)

                elif len(myarray) > 1:
                    i = 0
                    y = len(myarray)
                    # print(y)
                    for item in myarray:
                        if i == 0:
                            str1 = f"{item} {result_file}"
                            str = str1
                            # print(str)
                            i = i + 1
                        elif i >= 1:
                            str1 = f"{str} {item}"
                            i = i + 1
                            print(i)
                            str = str1
                            if i == len(myarray):
                                print(str)
                                cmd = str
                                subprocess.run([cmd], shell=True, stdout=f1)


# Running the functions
File1 = "/blah/scripts/INPUT/input.txt"
File2 = "/blah/scripts/INPUT/dir.txt"

with open(File1, 'r', encoding="utf-8") as t1:
    fileone = t1.readlines()
    # fileone = [item.strip(\n) for item in fileone]
    fileone = list(map(str.strip, fileone))
    print(fileone)

with open(File2, 'r', encoding="utf-8") as t2:
    filetwo = t2.readlines()
    # fileone = [item.strip(\n) for item in fileone]
    filetwo = list(map(str.strip, filetwo))
    print(filetwo)

for item in fileone:
    File = filetwo[1] + item
    final_result = filetwo[1] + "result_" + item.split(".")[0].lower() + ".log"
    result_file = filetwo[0] + item.split(".")[0] + ".csv"
    string_file = filetwo[0] + "mystrings_" + item.split(".")[0].lower() + ".csv"
    print(File, final_result, result_file, string_file)
    get_log()
    get_results()
