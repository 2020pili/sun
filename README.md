# Twilight, Golden Hour, Blue Hour, Magic Hour And Photography

File name: sun.py
Windows 10 user installation:
1. Search python 3.8 from Microsoft Store and install it.
2. Open DOC prompt to install PyEphem and GeoPy, etc.
    pip3 install pyephem    #https://rhodesmill.org/pyephem/toc.html
    pip install geopy       #https://geopy.readthedocs.io/en/latest/
    pip3 install pytz       #https://pypi.org/project/pytz/
    pip install pyowm       #https://pypi.org/project/pyowm/   https://openweathermap.org/api
3. Run the script
    python sun.py
4. Enter City name. and then it will show you when the Twilight, Golden Hour, Blue Hour happened. 
5. If your location is no city, please find one near you.
6. You need apply a free key from https://openweathermap.org/api for getting weather information.
   when you get your api key, you need update the key in keys.py file at the line Your_API_key = '12345yourapikey67890'
7. Reference https://www.timeanddate.com/sun/usa/san-francisco
8. You should have INTERNET access when you use the script. 
9. Please manually set the elevation in line "Viewpoint.elevation         = 10"   
