import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
import requests
from numpy.typing import NDArray


class TideInfo:
    def __init__(
        self,
        latitude: float,
        longitude: float,
        figure_size: tuple[float, float] = (10, 5),
    ):
        """Initialize the TideInfo class with location and plotting parameters."""
        self.latitude = latitude
        self.longitude = longitude
        self.figure_size = figure_size
        self.time_string_format = "%Y-%m-%dT%H:%M"
        self.api_caller = TideApiCaller()

    def _plot_tide(self, timestamps: NDArray, water_levels: NDArray):
        """Plot the tide levels over time using Matplotlib."""
        plt.figure(figsize=self.figure_size)
        plt.plot(timestamps, water_levels, marker="o")
        plt.title(
            f"Tide levels at Latitude {self.latitude:.2f}, Longitude {self.longitude:.2f}"
        )
        plt.xlabel("Time")
        plt.ylabel("Water Level (cm)")
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()
        plt.show()

    def plot_tide_time_series(self, start_time: str | None, end_time: str | None):
        """Fetch tide time series data and plot it."""
        # Set default start and end times if not provided
        if start_time is None:
            start_time = datetime.now().strftime(self.time_string_format)
        if end_time is None:
            end_time = (datetime.now() + timedelta(days=1)).strftime(
                self.time_string_format
            )

        # Get time series data and plot it
        timestamps, water_levels = self.api_caller.get_tide_time_series(
            self.latitude, self.longitude, start_time, end_time
        )
        self._plot_tide(timestamps, water_levels)

    def high_low_tide_str(self) -> str:
        """Return a string with the next high and low tide times."""
        start_time = datetime.now().strftime(self.time_string_format)
        end_time = (datetime.now() + timedelta(days=1)).strftime(
            self.time_string_format
        )
        next_high_tide, next_low_tide = self.api_caller.get_high_low_tides(
            self.latitude, self.longitude, start_time, end_time
        )
        # TODO: sort based on which comes first, format better
        return_str = f"Next high tide: {next_high_tide} \n"
        return_str += f"Next low tide: {next_low_tide}"

        return return_str


class TideApiCaller:
    def __init__(self, base_url="https://vannstand.kartverket.no/tideapi.php"):
        self.base_url = base_url
        self.time_string_format = "%Y-%m-%dT%H:%M"

    def _request_tide_info(
        self,
        latitude: float,
        longitude: float,
        start_time: str | None,
        end_time: str | None,
        datatype: Literal["pre", "tab"] = "pre",
    ) -> str:
        """Request tide information from the API.

        Parameters
        ----------
        latitude : float
            Latitude of the location for which to fetch tide information.
        longitude : float
            Longitude of the location for which to fetch tide information.
        start_time : str | None
            Start time for the tide data (in ISO format).
        end_time : str | None
            End time for the tide data (in ISO format).
        datatype : Literal["pre", "tab"], optional
            Data type to request, either "pre" for predicted tides (time series) or
            "tab" for astronomical high and low tides. By default "pre".

        Returns
        -------
        str
            The raw XML response from the tide API.
        """
        url = self.base_url
        params = {
            "lat": latitude,
            "lon": longitude,
            "fromtime": start_time,
            "totime": end_time,
            "datatype": datatype,
            "refcode": "cd",  # Reference code
            "interval": 10,  # Interval in minutes
            "dst": 0,  # Daylight saving time
            "tzone": 1,  # Time zone
            "tide_request": "locationdata",  # Tide request type
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.text

    def _parse_xml_time_series(
        self, xml_data: str
    ) -> tuple[NDArray[np.datetime64], NDArray[np.float64]]:
        """Parse the XML data to extract timestamps and water levels."""
        xml_root = ET.fromstring(xml_data)
        waterlevels = xml_root.findall(".//data/waterlevel")

        time = []
        levels = []
        for waterlevel in waterlevels:
            timestamp = waterlevel.attrib.get("time")
            value = waterlevel.attrib.get("value")
            if timestamp and value:
                time.append(timestamp)
                levels.append(float(value))

        time = np.array(time, dtype="datetime64[s]")
        levels = np.array(levels, dtype=float)

        return time, levels

    def _parse_xml_high_low_tides(
        self, xml_data: str
    ) -> tuple[tuple[str, float] | None, tuple[str, float] | None]:
        """Parse the XML data to extract the next high and low tide information."""
        xml_root = ET.fromstring(xml_data)
        waterlevels = xml_root.findall(".//data/waterlevel")

        next_high_tide = None
        next_low_tide = None

        for waterlevel in waterlevels:
            timestamp = waterlevel.attrib.get("time")
            value = waterlevel.attrib.get("value")
            tide = waterlevel.attrib.get("flag")

            if timestamp and value and tide:
                if tide == "high" and next_high_tide is None:
                    next_high_tide = (timestamp, float(value))
                elif tide == "low" and next_low_tide is None:
                    next_low_tide = (timestamp, float(value))
        return next_high_tide, next_low_tide

    def get_tide_time_series(
        self,
        latitude: float,
        longitude: float,
        start_time: str | None,
        end_time: str | None,
    ) -> tuple[NDArray[np.datetime64], NDArray[np.float64]]:
        """Fetch tide time series data and return timestamps and water levels."""
        xml_data = self._request_tide_info(
            latitude, longitude, start_time, end_time, datatype="pre"
        )
        return self._parse_xml_time_series(xml_data)

    def get_high_low_tides(
        self,
        latitude: float,
        longitude: float,
        start_time: str | None,
        end_time: str | None,
    ) -> tuple[tuple[str, float] | None, tuple[str, float] | None]:
        """Fetch high and low tide information and return the next high and low tides."""
        xml_data = self._request_tide_info(
            latitude, longitude, start_time, end_time, datatype="tab"
        )
        next_high_tide, next_low_tide = self._parse_xml_high_low_tides(xml_data)
        return next_high_tide, next_low_tide


if __name__ == "__main__":
    # Example usage
    latitude = 69.6498  # Tromsø, Norway
    longitude = 18.9841
    tide_info = TideInfo(latitude, longitude)
    tide_info.plot_tide_time_series(None, None)
    print(tide_info.high_low_tide_str())
