import subprocess

def append_new_data(file='flight_data.csv', include_header=False):
    """Append one line of csv location data to a file

    Keyword arguments:
    file -- the file where data will be appended; creates a new file if one doesn't already exist (default 'flight_data.csv')
    include_header -- set to True to append the header fields to the file (default False)
    """
    
    if include_header:
        header_arg = '1'
    else:
        header_arg = '0'
    
    # run the gpsd command to get the current location data
    args = ['gpscsv', '-n', '1', '--header', header_arg]
    cmd = subprocess.run(args, capture_output=True, text=True)
    
    # write the command output to the file
    with open(file, 'a') as f:
        f.write(cmd.stdout)
        f.close()
