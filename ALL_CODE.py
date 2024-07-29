import csv
from datetime import datetime, timedelta

##########################################################
def hex_to_decimal(hex_str):
    return int(hex_str, 16)

def GetBG(samps):
    background = 0
    accum = 0
    for samp in samps:
        accum += samp
    background = accum >> 6
    if background < 2:
        background = 2
        
    return background

def GetThresh(background):
    return int(7*(background**0.5) + background + 0.5)
##########################################################


"""
    Get TIME of an index
"""
def get_time(time_started, indices):
    # Parse the time_start string into a datetime object
    start_time = datetime.strptime(time_started, "%H:%M:%S %m-%d-%y")
    
    # Calculate time @ index
    current_times = []
    for index in indices:
        # Calculate the total elapsed time in seconds
        elapsed_seconds = index * 0.25
        
        # Calculate the end time by adding the elapsed time to the start time
        current_time = start_time + timedelta(seconds=elapsed_seconds)
        
        # Calculate the total elapsed time in days
        elapsed_days = elapsed_seconds / (24 * 3600)
    
    return {
        "elapsed_days": elapsed_days,
        "current_time": current_time
    }



def read_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        
        # Extract metadata
        time_started = rows[1][1].strip()
        tube_voltage = rows[2][1]
        calibration_factor = rows[3][1]
        
        # Extract raw_data and convert from hex to decimal
        raw_data = []
        for row in rows[4:]:
            raw_data.append(hex_to_decimal(row[1]))
        
    return {
        "raw_data": raw_data,
        "file_name": file_path.split('/')[-1],
        "time_start": time_started,
        "tube_voltage": tube_voltage,
        "calibration_factor": calibration_factor
    }

def get_peak(raw_data):
    BGCounts = 256
    background = GetBG(raw_data[0:BGCounts])
    threshold = GetThresh(background)
    
    peak_indices = []
    average_sample_graph = []
    background_graph = []
    threshold_graph = []
    
    in_pulse = False
    for i, value in enumerate(raw_data[BGCounts:], start=BGCounts):
        s0 = sum(raw_data[i-4:i])
        s1 = sum(raw_data[i-8:i-4])
        s2 = sum(raw_data[i-12:i-8])
        s3 = sum(raw_data[i-16:i-12])
        
        aveSamp = (s3 + 3 * (s2 + s1) + s0) >> 3
        
        average_sample_graph.append(aveSamp)
        
        if aveSamp > threshold and not in_pulse:
            in_pulse = True
            peak_indices.append(i)
            #print(f'{aveSamp}   {s0}   {s1}   {s2}   {s3}')
            
        elif aveSamp <= threshold and in_pulse:
            in_pulse = False
            
        temp = GetBG(raw_data[i-BGCounts:i])
        background = temp
        threshold = GetThresh(background)
            
        background_graph.append(temp)
        threshold_graph.append(threshold)
                                    
    return {
        "peak_indices": peak_indices,
        "average_sample_graph": average_sample_graph,
        "background_graph": background_graph,
        "threshold_graph": threshold_graph
    }

def get_text(raw_data):
    # Extract file name, start date, and start time
    file_name = raw_data['file_name']
    date_start = datetime.strptime(raw_data['time_start'], "%H:%M:%S %m-%d-%y").strftime("%m-%d-%y")
    time_start = datetime.strptime(raw_data['time_start'], "%H:%M:%S %m-%d-%y").strftime("%H:%M:%S")

    # Extract calibration factor and tube voltage
    calibration_factor = raw_data['calibration_factor']
    tube_voltage = raw_data['tube_voltage']

    # Calculate end date and end time using get_time function
    len_data = len(raw_data['raw_data'])
    indices = [len_data - 1]
    time_info = get_time(raw_data['time_start'], indices)

    date_end = time_info['current_time'].strftime("%m-%d-%y")
    time_end = time_info['current_time'].strftime("%H:%M:%S")

    # Return as a dictionary
    return {
        "file_name": file_name,
        "date_start": date_start,
        "time_start": time_start,
        "date_end": date_end,
        "time_end": time_end,
        "calibration_factor": calibration_factor,
        "tube_voltage": tube_voltage
    }
