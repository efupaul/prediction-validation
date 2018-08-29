@author Yifu Zhou
@Aug 29

# Space complexity
I create two lists data:
### pre_process_data 
After finishing reading two input files(actual and predicted), all the matched data will store here order by time.
[time, number of matched stockID, sum of these stock's diff]


[[1, 67, 0.0], [2, 74, 0.01], [3, 79, 0.01], [4, 75, 0.01], [5, 77, 0.01], ...]

### comparison

It stores the data what output file will look like

['1|4|0.00', '2|5|0.00', '3|6|0.00', '4|7|0.00', '5|8|0.00', '6|9|0.00', ...]

# Time complexity

1. I save all the data in actual.txt into dict(), and combine time and stockID as key. 
2. Through the time-stockID key, find the matched data in predicted.txt and save these data into the form of pre_process_data, so the look up function is O(n)
3. The comparison_sliding_window is the function to transform pre_process_data to comparison, time complexity is O(n) which n = number of lines in output_file = end_time - start_time - window_side + 1
