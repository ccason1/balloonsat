from gps import *
import time
import csv

class GnssDataGetter:

    def __init__(self, *data_output_options, filename='flight_data.csv'):
        self.data_output_options = list(data_output_options)
        self.session = gps(mode=WATCH_ENABLE)
        self.output_file = open(filename, 'a')
        self.writer = csv.writer(self.output_file)

    def get_report(self):
        report = None
        try:
            report = self.session.next()
            if report['class'] == 'DEVICE':
                self.session.close()
                self.session = gps(mode=gps)
        except StopIteration:
            print("GPSD has terminated")
        
        return report
    
    def write_data(self, timeout_sec=1.5, write_header=False):
        report = self.get_report()
        start = time.time()
        
        # class TPV is the only class that contains the data we want
        # the following link has information about TPV and the other gpsd classes
        # gpsd.gitlab.io/gpsd/gpsd_json.html
        while report['class'] != 'TPV':
            report = self.get_report()
            if time.time() - start > timeout_sec:
                print('timeout')
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
        self.output_file.close()
        

def main():
    dg = GnssDataGetter('time', 'lat', 'hi', 'lon')
    dg.write_data(write_header=True)
    dg.close_file()
    

if __name__ == '__main__':
    main()



