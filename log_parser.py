#!/usr/bin/env python3
'''
Script to parse smf log files , script is using config file in csv format,
the config file is  mystrings.csv
file format is
string1,string2,string3

script will generate grep  as follows
grep -E 'string1' what_ever.csv|grep -E  'string2'|grep -E 'string3'

'''

from datetime import datetime, timedelta
import subprocess
import csv

final_result = "/what_ever/log/result_rtc.log"
File = "/what_ever/log/what_ever.log"
result_file = "/what_ever/scripts/what_ever.csv"
string_file = "/what_ever/scripts/mystrings_rtc.csv"


def get_log():
    '''
    Function to get last 5 minutes log
    '''
    now = datetime.now()
    print(now)
    lookback = timedelta(minutes=5)
    print(lookback)
    five_min_before = (now - lookback).strftime("%b %e %H:%M:%S")
    print(five_min_before)

    file_object = open(result_file, 'w')
    f = open(File, "r")
    for line in f:
        if line[:14] > five_min_before:
            # print(line)
            file_object.write(line)

    f.close()
    file_object.close()


def get_files():
    '''
    This function is not used yet, we can use it in the Future,
    if we need to generate any stats using pandas
    '''
    subprocess.call("awk -F: '{print NF}' what_ever.csv |sort -nu|\
    while read line;\
    do awk -F: '(NF=='$line') {print }' what_ever.csv  >what_ever_${line}.csv;done ",
                    shell=True)

    cmd = "ls what_ever_*.csv"
    output = subprocess.run(cmd, shell=1, stdout=subprocess.PIPE).stdout.decode('utf-8')

    file_list = output.split()
    print(file_list)


def get_results():
    '''
    function to  get the grep command
    '''

    f1 = open(final_result, "a+")
    csv_file = open(string_file, "r")
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:
        myarray1 = row
        myarray = list(filter(None, myarray1))

        print(len(myarray))
        i = 0

        for n in range(len(myarray)):
            if i == 0:
                stri = myarray[n]
                print(i)
                i = i + 1
                str0 = " grep -E "
                print(str0)
                str1 = stri

                str3 = f"{str0} '{str1}'  {result_file}"
                str1 = str3
                print(str1)
                cmd = str1
              
                subprocess.run([cmd], shell=True, stdout=f1)
            elif i > 0:
                stri = myarray[n]
                str2 = " | grep -E " + f"'{stri}'"
                str3 = f"{str1} {str2}"
                str1 = str3
                i = i + 1
                print(str1)
                cmd = str1
                subprocess.run([cmd], shell=True, stdout=f1)

    csv_file.close()
    f1.close()


# Running the functions
get_log()
get_results()