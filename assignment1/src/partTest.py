import csv

def create_equiwidth_histogram(data, bins):
    min_value = min(data)
    max_value = max(data)
    bin_width = (max_value - min_value) / bins
    bins_list = [min_value + i * bin_width for i in range(bins+1)]
    hist = [0] * bins
    for d in data:
        bin_index = int((d - min_value) // bin_width)
        if bin_index == bins:
            bin_index -= 1
        hist[bin_index] += 1
    return hist, bins_list

def create_equidepth_histogram(data, num_bins):
    sorted_data = sorted(data)
    n = len(data)
    bin_size = n // num_bins
    remainder = n % num_bins

    bins_list = []
    hist = []
    start = 0
    for i in range(num_bins):
        if i == num_bins - 1:
            end = n
        else:
            end = start + bin_size
            if i >= num_bins - remainder:
                end += 1

        bins_list.append(sorted_data[start])
        hist.append(end - start)

        if i == num_bins - 1:
            bins_list.append(sorted_data[end - 1])

        start = end

    return hist, bins_list

def estimate_tuples_exact(hist, bins_list, a, b):
    count = 0
    for i in range(len(bins_list)-1):
        if b <= bins_list[i]:
            break
        if a < bins_list[i+1]:
            percentage = (min(b, bins_list[i+1]) - max(a, bins_list[i])) / (bins_list[i+1] - bins_list[i])
            count += percentage * hist[i]
    return count


def main():

    filename = input("Enter the filename: ")
    fieldname = input("Enter the field name: ")
    a = int(input("Enter a: "))
    b = int(input("Enter b: "))
    num_bins = 100

    data = []
    with open(filename) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            try:
                data.append(float(row[fieldname]))
            except ValueError:
                pass

    print("%d valid values" %(len(data)))
    print("minimum value = %.1f, maximum value = %.1f " % (min(data),max(data)))

    equi_width_hist_data, equi_width_hist_edges = create_equiwidth_histogram(data, num_bins)
    print("equi-width histogram:")
    for i in range(num_bins):
        print("[%.2f, %.2f), numtuples: %d" %(equi_width_hist_edges[i],equi_width_hist_edges[i+1],equi_width_hist_data[i]))

    equi_depth_hist_data, equi_depth_hist_edges = create_equidepth_histogram(data, num_bins)
    print("\nequi-depth histogram:")
    for i in range(num_bins):
        print("[%.2f, %.2f), numtuples: %d" %(equi_depth_hist_edges[i],equi_depth_hist_edges[i+1],equi_depth_hist_data[i]))

    count_eqw = estimate_tuples_exact(equi_width_hist_data, equi_width_hist_edges, a, b)
    print("\nequi-width histogram estimated results: %f" % count_eqw)
    count_eqd = estimate_tuples_exact(equi_depth_hist_data, equi_depth_hist_edges, a, b)
    print("equi-depth histogram estimated results: %f" % count_eqd)
    actual_count = len([d for d in data if a <= d < b])
    print(f"Actual results: {actual_count}")



if __name__ == "__main__":
    main()
