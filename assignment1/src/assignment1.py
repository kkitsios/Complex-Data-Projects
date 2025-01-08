# Konstantinos Kitsios, AM: 4388
# How to execute:
# python3 assignment1.py <filename> <fieldname>

import csv
import sys

def equiwidth_histogram(data, bins):
    min_value = min(data)
    max_value = max(data)
    bin_width = (max_value - min_value) / bins
    bins_ranges = [min_value + i * bin_width for i in range(bins+1)]
    hist_data = [0] * bins
    for d in data:
        bin_index = int((d - min_value) // bin_width)
        if bin_index == bins:
            bin_index -= 1
        hist_data[bin_index] += 1
    return hist_data, bins_ranges

def equidepth_histogram(data, bins):
    sorted_data = sorted(data)
    n = len(data)
    bin_size = n // bins
    remainder = n % bins

    bins_ranges = []
    hist_data = []
    start = 0
    for i in range(bins):
        if i == bins - 1:
            end = n
        else:
            end = start + bin_size
            if i >= bins - remainder:
                end += 1

        bins_ranges.append(sorted_data[start])
        hist_data.append(end - start)

        if i == bins - 1:
            bins_ranges.append(sorted_data[end - 1])

        start = end

    return hist_data, bins_ranges

def estimate_tuples(hist_data, bins_ranges, a, b):
    count = 0
    for i in range(len(bins_ranges)-1):
        if b <= bins_ranges[i]:
            break
        if a < bins_ranges[i+1]:
            percentage = (min(b, bins_ranges[i+1]) - max(a, bins_ranges[i])) / (bins_ranges[i+1] - bins_ranges[i])
            count += percentage * hist_data[i]
    return count

def data_load(data,filename,fieldName):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                data.append(float(row[fieldName]))
            except ValueError:
                pass

def main():

    args = sys.argv[1:]
    filename = args[0]
    fieldName = args[1]

    bins_number = 100
    data =[]

    data_load(data,filename,fieldName)

    print("\n----------------------------------------------\n")
    print("%d valid values" % (len(data)))
    print("minimum value = %.1f, maximum value = %.1f " % (min(data),max(data)))

    #Equi-width histogram printing
    equiwidth_data, equiwidth_ranges = equiwidth_histogram(data, bins_number)
    print("equiwidth histogram:")
    for i in range(bins_number):
        print("[%.2f, %.2f), numtuples: %d" %(equiwidth_ranges[i],equiwidth_ranges[i+1],equiwidth_data[i]))

    #Equi-depth histogram printing
    equidepth_data, equidepth_ranges = equidepth_histogram(data, bins_number)
    print("\nequidepth histogram:")
    for i in range(bins_number):
        print("[%.2f, %.2f), numtuples: %d" %(equidepth_ranges[i],equidepth_ranges[i+1],equidepth_data[i]))


    #Tuples estimation
    print("\n-------------------------------------\n")
    print("Enter a, b ranges for estimation, press ctrl + c for exit if you don't want to try multiple values.\n")

    try:
        while True:

            a = int(input("Enter a: "))
            b = int(input("Enter b: "))

            if(a < b):
                equiwidth_est = estimate_tuples(equiwidth_data, equiwidth_ranges, a, b)
                equidepth_est = estimate_tuples(equidepth_data, equidepth_ranges, a, b)
                actual_tuples = len([d for d in data if a <= d < b])

                print("\nequi-width histogram estimated results: %f" % equiwidth_est)
                print("equi-depth histogram estimated results: %f" % equidepth_est)
                print("Actual results: %d\n" % actual_tuples)
            else:
                print("Error! Range must be [a,b), you gave b > a. Try again.\n")
    except KeyboardInterrupt:
        print("\nExiting program.")


if __name__ == "__main__":
    main()