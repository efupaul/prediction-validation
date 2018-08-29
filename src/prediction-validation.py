import argparse

def process_data(pre_process_data, actual_file_path, predicted_file_path):
    actual_data = dict()
    try:
        file = open(actual_file_path, 'r')
    except IOError:
        print "Error: cannot find actual file"
    else:
        lines = file.readlines()
        for line in lines:
            temp = line.strip('\n').split("|")
            # combine time + stockID as key
            actual_data[temp[0] + temp[1]] = float(temp[2])
        file.close()

    # print actual_data

    try:
        file = open(predicted_file_path, 'r')
    except IOError:
        print "Error: cannot find predicted file"
    else:
        lines = file.readlines()
        list = []
        index = 0
        for line in lines:
            temp = line.strip('\n').split("|")
            if int(temp[0]) != index:
                index = int(temp[0])
                if list:
                    pre_process_data.append(list)
                list = [index, 0, 0]
            if actual_data.has_key(temp[0] + temp[1]):
                diff = abs(actual_data[temp[0] + temp[1]] - float(temp[2]))
                list[1] += 1
                list[2] += diff
                #Use a trick way to avoid floating-point numeric errors
                list[2] = float(str('%.2f' % list[2]))

        pre_process_data.append(list)
        file.close()

def comparison_sliding_window(comparison, window_file_path, pre_process_data):
    """
    design an algorithm which time complexity is O(n),
    n = number of lines in output_file = end_time - start_time - window_side + 1
    """
    window_side = 0
    try:
        file = open(window_file_path, 'r')
    except IOError:
        print "Error: cannot find window file"
    else:
        lines = file.readlines()
        for line in lines:
            window_side = int(line.strip('\n'))
        file.close()

        num = 0
        sum = 0
        start_time = pre_process_data[0][0]
        begin_index = 0
        for index in range(len(pre_process_data)):
            if pre_process_data[index][0] >= start_time and pre_process_data[index][0] < start_time + window_side:
                num += pre_process_data[index][1]
                sum += pre_process_data[index][2]
            else:
                each = str(start_time) + "|" + str(start_time + window_side - 1) + "|" + str('%.2f' % (sum / num))
                comparison.append(each)
                start_time += 1
                while True:
                    if pre_process_data[begin_index][0] < start_time:
                        num -= pre_process_data[begin_index][1]
                        sum -= pre_process_data[begin_index][2]
                        begin_index += 1
                    if pre_process_data[index][0] >= start_time and pre_process_data[index][0] < start_time + window_side:
                        num += pre_process_data[index][1]
                        sum += pre_process_data[index][2]
                        break
                    else:
                        if num == 0:
                            sub = str(start_time) + "|" + str(start_time + window_side - 1) + "|NA"
                        else:
                            sub = str(start_time) + "|" + str(start_time + window_side - 1) + "|" + str('%.2f' % (sum / num))
                        comparison.append(each)
                    start_time += 1
        each = str(start_time) + "|" + str(start_time + window_side - 1) + "|" + str('%.2f' % (sum / num))
        comparison.append(each)

def write_output_file(output_file_path, comparison):
    file = open(output_file_path, 'w')
    for i in comparison:
        file.write(i)
        file.write("\n")
    file.close()

if __name__ == '__main__':
    # Setup command line Argumnets.
    parser = argparse.ArgumentParser()
    parser.add_argument('window_file_path', help='the path of window.txt.')
    parser.add_argument('actual_file_path', help='the path of actual.txt.')
    parser.add_argument('predicted_file_path', help='the path of predicted.txt.')
    parser.add_argument('output_file_path', help='the path of output file.')

    # Parse arguments
    args = parser.parse_args()
    window_file_path = args.window_file_path
    actual_file_path = args.actual_file_path
    predicted_file_path = args.predicted_file_path
    output_file_path = args.output_file_path

    # ceate pre_process data, the form will be like: [time, number of matched stock, the sum of these stock difference]
    pre_process_data = []
    process_data(pre_process_data, actual_file_path, predicted_file_path)
    #print pre_process_data

    # Save the final data what the output file looks like
    comparison = []
    comparison_sliding_window(comparison, window_file_path, pre_process_data)
    #print comparison

    write_output_file(output_file_path, comparison)
