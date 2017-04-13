from datetime import *

from plotly import *

class TimeSeries(object):
    """
    Representation of a time series
    """
    def __init__(self, name, data, datetime_format=None):
        self._name = str(name)
        self._data = {}

        if datetime_format is None:
            datetime_format = "%Y-%m-%dT%H:%M:%S"

        for pair in data:
            self._data[datetime.strptime(pair[0], datetime_format)] = pair[1]

    """
    The name of the time series
    """
    @property
    def name(self):
        return self._name

    """
    The underlying data as a dictionary whose keys are timestamps
    """
    @property
    def data(self):
        return self._data

    """
    Adds a new entry to the time series (where entry is a 2-tuple)
    """
    def add(self, entry):
        self._data[entry[0]] = entry[1]

    """
    Removes the specified entry from the time series
    """
    def remove(self, time):
        self._data.pop(time)

    def __getitem__(self, key):
        return self.data[key]

    def __contains__(self, item):
        if item in self.data:
            return True
        else:
            return False

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        s = ""

        for k, v in self.data.items():
            s += str(k) + " " + str(v) + "\n"

        return s

    def _plot_layout(self):
        return graph_objs.Layout(title=self.name, xaxis={"title": "Time"})

    def plot(self):
        data = []
        pairs = []
        x_data = []
        y_data = []

        for k, v in self.data.items():
            pairs.append((k, v))

        for p in sorted(pairs, key=lambda x: x[0]):
            x_data.append(p[0])
            y_data.append(p[1])
        
        trace = graph_objs.Scatter(
            x=x_data,
            y=y_data)

        layout = self._plot_layout()
        
        data = [trace]
        figure = graph_objs.Figure(data=data, layout=layout)

        offline.plot(figure)

class ABSTimeSeries(TimeSeries):
    """
    A representation of a time series from the Australian Bureau of Statistics
    """
    def __init__(self, name, unit, series_type, data_type, frequency,
                 collection_month, series_start, series_end, num_obs,
                 series_id, data):
        super().__init__(name, data, "%b-%Y")
        
        self._unit = str(unit)
        self._series_type = str(series_type)
        self._data_type = str(data_type)
        self._frequency = str(frequency)
        self._collection_month = str(collection_month)
        self._series_start = series_start
        self._series_end = series_end
        self._num_obs = int(num_obs)
        self._series_id = str(series_id)

    """
    The unit that the values of the time series are in
    """
    @property
    def unit(self):
        return self._unit
    
    """
    The type of time series
    """
    @property
    def series_type(self):
        return self._series_type

    """
    The type of data the time series stores (according to the ABS)
    """
    @property
    def data_type(self):
        return self._data_type

    """
    The frequency that the ABS collects data on
    """
    @property
    def frequency(self):
        return self._frequency

    """
    The month the ABS collects data for this time series
    """
    @property
    def collection_month(self):
        return self._collection_month

    """
    The start of the time series (according to the ABS)
    """
    @property
    def series_start(self):
        return self._series_start

    """
    The end of the time series (according to the ABS)
    """
    @property
    def series_end(self):
        return self._series_end

    """
    The number of observations in the time series (according to the ABS)

    Note that this is not necessarily equal to the actual size of the time
    series (for bounds-checking purposes, use len())
    """
    @property
    def num_obs(self):
        return self._num_obs

    """
    The ID assigned to the time series by the ABS
    """
    @property
    def series_id(self):
        return self._series_id

    def __str__(self):
        return self.name + " (" + self.series_id + ")"

    def _plot_layout(self):
        return graph_objs.Layout(title=self.name, xaxis={"title": "Time"}, yaxis={"title": self.unit})


