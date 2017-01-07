#!/usr/bin/env python
# Program is created by Jakub Kubista to Distributed Systems : Big Exercise 4
# and it's based on script for Spark assignments by Liang Wang @ CS Dept
# Helsinki University, Finland
#

import os
import sys
import time

### Dataset
DATA1 = '/cs/work/scratch/spark-data/data-1.txt'
DATA1_SAMPLE = '/cs/work/scratch/spark-data/data-1-sample.txt'
H_DATA_10 = 'h-data-10.txt'
H_DATA_100 = 'h-data-100.txt'
H_DATA_1000 = 'h-data-1000.txt'

### Some variables you may want to personalize
AppName = "DS: Big Exercise 4 - Spark example"
TMPDIR = "/cs/work/scratch/spark-tmp"

### Creat a Spark context on Ukko cluster
from pyspark import SparkConf, SparkContext
conf = (SparkConf()
        .setMaster("spark://ukko007:7077")
        .setAppName(AppName)
        .set("spark.rdd.compress", "true")
        .set("spark.broadcast.compress", "true")
        .set("spark.cores.max", 10)  # do not be greedy :-)
        .set("spark.local.dir", TMPDIR))
sc = SparkContext(conf = conf)

### TASK 1

### Function for calculate average from file after mapping
def calculate_average(fn):
    data = sc.textFile(fn)
    data = data.map(lambda s: float(s))
    myAvg = data.sum() / data.count()
    return myAvg

### Function for calculate average from file after mapping by mean function
# mean is the sum of all the numbers in the set divided by the amount of numbers in the set.
def calculate_average_alternative(fn):
    data = sc.textFile(fn)
    avg_value = data.map(lambda s: float(s)).mean()
    return avg_value

### Function for calculate average from file without Spark
def calculate_average_without_spark(fn):
    sum_f = 0.0
    i = 0
    try:
        with open(fn,"r") as f:
            for line in f:
                sum_f += float(line)
                i += 1
        f.close()

    except IOError:
        raise Exception('IO exeption - Unreadable file')
    return sum_f/i


### Function for calculate min from file after mapping
def calculate_min(fn):
    data = sc.textFile(fn)
    min_value = data.map(lambda s: float(s)).min()
    return min_value

### Function for calculate max from file after mapping
def calculate_max(fn):
    data = sc.textFile(fn)
    max_value = data.map(lambda s: float(s)).max()
    return max_value

### Function for calculate variance from file after mapping
def calculate_variance(fn):
    data = sc.textFile(fn)
    variance_value = data.map(lambda s: float(s)).variance()
    return variance_value

### Function which calculate all previous functions together to save time
def calculate_four_functions(fn):
    data = sc.textFile(fn)
    data = data.map(lambda s: float(s))
    myAvg = data.sum() / data.count()
    min_value = data.min()
    max_value = data.max()
    variance_value = data.variance()
    return myAvg, min_value, max_value, variance_value

### TASK 2

# It's simple to compute Mode - just the value that shows the most.
# I tried at first use mode from statistics library, but we are working with
# low version of python, then I implement following function mode which
# I wanted call from calculate_mode, but RDD / map objects are not iterable.
# I also tried to do it by Counter together with Spark, but also not good result
# For sure I did a classic function calculate_mode_without_spark, what works with sample data,
# but with big one it was MemoryError.

from collections import Counter

### Function for find mode by Spark spark function
def mode(array,a_count):
    most = max(list(map(a_count, array)))
    return list(set(filter(lambda x: a_count(x) == most, array)))

### Function for preparing data and choose first mode
def calculate_mode_spark(fn):
    data = sc.textFile(fn)
    # data = data.map(lambda s: float(s))
    data = data.map(Counter).reduce(lambda x, y: x + y)
    # mode_value = mode2(data,data.count())
    mode_value = data.most_common(1)
    return mode_value

### Function for calculate mode withou Spark
def calculate_mode_without_spark(fn):
    data = []
    try:
        with open(fn,"r") as f:
            for line in f:
                data.append(float(line))
        f.close()
        data = Counter(data)

    except IOError:
        raise Exception('IO exeption - Unreadable file')
    return data.most_common(1)[0][0]

### TASK 3

### Procedure produce an output file that has n (10,100,1000) lines
### Basically it create integer on each line.

def write_to_histogram_file(data,fn):
    try:
        with open(fn,"w+") as f:
            for item in data:
                f.write("%s\n" % item)  #  writing row by row
        f.close()
    except IOError:
        raise Exception('IO exeption - Unreadable file')


# numpy.np library is for integer arguments the function is equivalent to the Python
import numpy as np

### Function, which calculate histogram with n bins
def calculate_histogram(fn, hfn,n): #hfn = histogram file name
    # Linspace functionReturn evenly spaced numbers over a specified interval
    # it's basicly decimal range() step value function,
    # which lets you have control over what happens at the endpoin.
    # But after that is necessary to change linspace into array.

    histo_array = []
    histo_lin = np.linspace(0,100,n+1)  # range 0-100, n = 10, 100, 1000
    for i in range(len(histo_lin)):
        histo_array.append(histo_lin[i])

    data = sc.textFile(fn)
    histogram_data = data.map(lambda s: float(s)).histogram(histo_array)
    write_to_histogram_file(histogram_data[1],hfn)  # [1] = we want to use only histogram data
    return histogram_data[1]

### Function, which calculate execution time of different average function.
### Returns average
def time_of_execution_avg(data):
    start_time = time.time()
    myAvg = calculate_average(data)
    print("Time of execution for avg with Spark (original): " + str(time.time() - start_time) + " seconds")

    start_time = time.time()
    calculate_average_alternative(data)
    print("Time of execution for avg with Spark (alternative): " + str(time.time() - start_time) + " seconds")

    start_time = time.time()
    calculate_average_without_spark(data)
    print("Time of execution for avg without Spark: " + str(time.time() - start_time) + " seconds")
    return myAvg

### Main function

if __name__=="__main__":
    # In addition: time of execution for different average functions.
    # myAvg, myAvg_alternative = time_of_execution_avg(DATA1)

    # Calling functions for task 1 for projects:
    # myMin = calculate_min(DATA1)
    # myMax = calculate_max(DATA1)
    # myVar = calculate_variance(DATA1)

    # Calling functions for task 1 for this exercise:
    start_time = time.time()
    myAvg, myMin, myMax, myVar = calculate_four_functions(DATA1)
    print("Time of execution for functions: " + str(time.time() - start_time) + " seconds")

    # Printing task 1,2 for sure
    print "Average = %.8f" % myAvg
    # print "Average alternative = %.8f" % myAvg_alternative
    print "Minumum = %.8f" % myMin
    print "Maximum = %.8f" % myMax
    print "Variance = %.8f" % myVar

    # Check for task 2 - not working with data-1, only with sample
    # myMode = calculate_mode_without_spark(DATA1)
    # print "Mode = %.8f" % myMode

    # Produce output files with histograms for task 3
    myhistogram_ten = calculate_histogram(DATA1, H_DATA_10, 10)
    myhistogram_hundred = calculate_histogram(DATA1, H_DATA_100, 100)
    myhistogram_thousand = calculate_histogram(DATA1, H_DATA_1000, 1000)


    sys.exit(0)
