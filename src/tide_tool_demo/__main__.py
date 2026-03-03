from .tide_tool_demo import TideInfo

latitude = 69.6498  # Tromsø, Norway
longitude = 18.9841
tide_info = TideInfo(latitude, longitude)

print("Tide Tool Demo - Example Usage")
print("Next high and low tide information for Tromsø, Norway:")
print(tide_info.high_low_tide_str())
