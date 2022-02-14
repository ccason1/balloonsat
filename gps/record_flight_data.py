# Example:
# dg = GnssDataGetter('time', 'lat', 'lon', 'altHAE', filename='data.csv')
# dg.write_data(write_header=True)
# dg.write_data()
#
# output:
# time,lat,lon,altHAE
# 2022-02-14T15:51:52.000Z,39.1234567,-105.1234567,1716.123
# 2022-02-14T15:51:53.000Z,39.2234567,-105.2234567,1716.456 
#
# The format of the time is ISO8601 format:
# [yyyy]-[mm]-[dd]T[hh]:[mm]:[ss].000Z where the Z at the end indicates UTC
# See the following Wikipedia article for more info:
# https://en.wikipedia.org/wiki/ISO_8601

from gps import *
import time
import csv

class GnssDataGetter:
    """A class to retrieve data from a GNSS receiver and append it to a csv file.
    
    Attributes:
    *data_output_options
        determines which data will be written to the file;
        refer to https://gpsd.io/gpsd_json.html for information about the options.
    filename
        the output file; can include path (default 'flight_data.csv')
    """
    
    def __init__(self, *data_output_options, filename='flight_data.csv'):
        
        self.data_output_options = list(data_output_options)
        self.session = gps(mode=WATCH_ENABLE)
        self.output_file = open(filename, 'a')
        self.writer = csv.writer(self.output_file)

    def get_report(self):
        """Return a dictionary-like object containing a packet of GNSS data"""
        
        report = None
        try:
            report = self.session.next()
            if report['class'] == 'DEVICE':
                self.session.close()
                self.session = gps(mode=gps)
        except StopIteration:
            return
        
        return report
    
    def write_data(self, timeout_sec=2, write_header=False):
        """Write the current GNSS data to a csv file.
       
       Keyword arguments:
         timeout
             time in seconds to allow data retrieval before breaking (default 2)
         write_header 
             writes the fields to the csv as a header; do this on the first run (default False)
       """
    
        report = self.get_report()
        start = time.time()
        
        # class TPV is the only class that contains the data we want
        # the following link has information about TPV and the other gpsd classes
        # gpsd.gitlab.io/gpsd/gpsd_json.html
        while report['class'] != 'TPV':
            report = self.get_report()
            if time.time() - start > timeout_sec:
                return
        
        header = self.data_output_options
        
        if write_header:
            print(header)
            self.writer.writerow(header)
        
        vals = []
        for key in header:
            if key in list(report):
                vals.append(report[key])
            else:
                vals.append('')
        
        self.writer.writerow(vals)
        print(vals)
        
    def close_file(self):
        """Close the output_file--this function should be called after the final write operation"""
    
        self.output_file.close()
        

def main():
    dg = GnssDataGetter('time', 'lat', 'hi', 'lon')
    dg.write_data(write_header=True)
    dg.write_data()
    dg.close_file()
    

if __name__ == '__main__':
    main()
