#!/usr/bin/env python3
'''
Script to parse log files , script is using config file in csv format,
the config file is  mystrings.csv
file format is
string1,string2,string3

script will generate grep  as follows
grep -E 'string1' blah.csv|grep -E  'string2'|grep -E 'string3'

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
    print(five_min_before)
    File = "/var/opt/blah/log/blah.log"
    file_object = open('/var/opt/blah/scripts/blah.csv', 'w')
    f = open(File, "r")
    for line in f:
        if line[:14] > five_min_before:
            # print(line)
            file_object.write(line)

    f.close()
    file_object.close()


def get_files():
    '''
    This function is not used yet, we can use it in Future,
    if we need to generate any stats using pandas
    '''
    subprocess.call("awk -F: '{print NF}' blah.csv |sort -nu|\
    while read line;\
    do awk -F: '(NF=='$line') {print }' blah.csv  >blah_${line}.csv;done ",
                    shell=True)

    cmd = "ls blah_*.csv"
    output = subprocess.run(cmd, shell=1, stdout=subprocess.PIPE).stdout.decode('utf-8')

    file_list = output.split()
    print(file_list)


def get_results():
    '''
    function to  get the grep command
    '''

    f = open("/var/opt/blah/log/result.log", "a")
    csv_file = open('/var/opt/blah/scripts/mystrings.csv')
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
                str1=stri

                str3 = f"{str0} '{str1}'  /var/opt/blah/scripts/blah.csv "
                str1 = str3
                print(str1)
                cmd = str1
                subprocess.run([cmd], shell=True, stdout=f)
            elif i > 0:
                stri = myarray[n]
                str2 = " | grep -E " + f"'{stri}'"
                str3 = f"{str1} {str2}"
                str1 = str3
                i = i + 1

                # print(str1)
                cmd = str1
                print(cmd)
                subprocess.run([cmd], shell=True, stdout=f)

    f.close()
    csv_file.close()


# Running the functions
get_log()
get_results()