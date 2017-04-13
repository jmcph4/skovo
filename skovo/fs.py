import ts

class TimeSeriesCSVFile(object):
    def __init__(self, filename, delim=None):
        self._filename = filename
        
        if delim is None:
            self._delim = ","
        else:
            self._delim = delim

    @property
    def filename(self):
        return self._filename

    @property
    def delim(self):
        return self._delim

    def __repr__(self):
        with open(self.filename) as f:
            return str(f)

    def load(self, skip_invalid_lines=None):
        if skip_invalid_lines is None:
            skip_invalid_lines = False
        
        name = self.filename[:self.filename.find(".")]
        data = []
        
        with open(self.filename) as csv_file:
            for line in csv_file:
                if line.count(self.delim) == 1:
                    data.append(line.split(self.delim))
                else:
                    if skip_invalid_lines == False:
                        raise InvalidFileFormatException()

        return ts.TimeSeries(name, data)
                    
class ABSTimeSeriesCSVFile(TimeSeriesCSVFile):
    def __init__(self, filename, delim=None):
        super().__init__(filename, delim)

        self._num_metadata_lines = 10

    def load(self, skip_invalid_lines=False):
        if skip_invalid_lines is None:
            skip_invalid_lines = False
            
        data = []
        line_num = 0

        name = ""
        unit = ""
        series_type = ""
        data_type = ""
        frequency = ""
        collection_month = ""
        series_start = ""
        series_end = ""
        num_obs = ""
        series_id = ""
        
        with open(self.filename) as csv_file:
            for line in csv_file:
                clean_line = line.strip(self.delim)
                clean_line = clean_line.strip("\n")

                # read ABS metadata
                if line_num < self._num_metadata_lines:
                    if line.count(self.delim) == 1:
                        if line_num == 0:
                            name = clean_line
                        elif line_num == 1:
                            unit = clean_line
                        elif line_num == 2:
                            series_type = clean_line
                        elif line_num == 3:
                            data_type = clean_line
                        elif line_num == 4:
                            frequency = clean_line
                        elif line_num == 5:
                            collection_month = clean_line
                        elif line_num == 6:
                            series_start = clean_line
                        elif line_num == 7:
                            series_end = clean_line
                        elif line_num == 8:
                            num_obs = int(clean_line)
                        elif line_num == 9:
                            series_id = clean_line
                    else:
                        if skip_invalid_lines == False:
                            raise InvalidFileFormatException()
                else:
                    if line.count(self.delim) == 1:
                        data.append(line.split(self.delim))
                    else:
                        if skip_invalid_lines == False:
                            raise InvalidFileFormatException()
                line_num += 1

        return ts.ABSTimeSeries(name, unit, series_type, data_type, frequency,
                         collection_month, series_start, series_end, num_obs,
                         series_id, data)
