# Copyright 2014 Au Yeong Wing Yau
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
A file stores time durations in the following format where every line is a duplicated again:

0:01:56
0:01:56
0:21:46
0:21:46
0:21:53
0:21:53
0:11:48
0:11:48
0:21:47
0:21:47
0:07:55
0:07:55

This application parses the file, removes duplicates, change time to a numerical value, e.g. 0:01:50 = 1.833. Then collects the results into a separate target file where the results are tallied up as follows:

Less than 3 minutes: 
3-6 minutes:
6-9 minutes:
.
.
.
More than 21 minutes:

A graphing or histogram application will be able to use the generated file to create graphs or data analysis.

Usage:
python data_prep.py ORIGINAL_FILE

Results will be written to new file ORIGINAL_FILE.prep
"""

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

ORIGINAL_FILE = str(sys.argv[1])
TARGET_FILE = ORIGINAL_FILE+".prep"
range_list= [0] * 8


# Read data from original file
filehandler = open(ORIGINAL_FILE, "r")
text_list = filehandler.readlines()
filehandler.close()


for i in range(len(text_list)):
	if i % 2 == 0: # We have duplicates in this list, skip every second line.
		tmp_txt = text_list[i].strip('\r\n\0') # Strip out unwanted trailing chars.
		split_txt = tmp_txt.split(":") # Split the hh:mm:ss time components 
		time = float(split_txt[0])*60 + float(split_txt[1]) + float(split_txt[2])/60.0 # Convert the components to numerical minutes e.g. 0:1:50 = 1.83
		
		# Fill the numbers in the range_list.
		index = int(time/3.0) # Split the values into segments of 3.
		if index > 7: # All values more than 21 minutes.
			index = 7
		range_list[index] = range_list[index] + 1


print range_list


# Write results to TARGET_FILE.
filehandler = open(TARGET_FILE, "w")

filehandler.write("Less than 3 minutes:"+str(range_list[0])+"\n")
filehandler.write("3-6 minutes:"+str(range_list[1])+"\n")
filehandler.write("6-9 minutes:"+str(range_list[2])+"\n")
filehandler.write("9-12 minutes:"+str(range_list[3])+"\n")
filehandler.write("12-15 minutes:"+str(range_list[4])+"\n")
filehandler.write("15-18 minutes:"+str(range_list[5])+"\n")
filehandler.write("18-21 minutes:"+str(range_list[6])+"\n")
filehandler.write("More than 21 minutes:"+str(range_list[7])+"\n")

filehandler.close()
