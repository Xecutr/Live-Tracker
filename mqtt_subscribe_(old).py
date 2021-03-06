# Necessary libraries and packages:
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import math
import numpy
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# defining constants to calculate the distance:
radius = 6371000
p = 0.017453292519943295
latdata, longdata = [], []

# Getting the lat-long:
chrome_options = Options()
driver = webdriver.Chrome()
driver.set_window_size(700, 700)
print("Setting up the Subscriber .... ")

# Opening Google maps:
driver.get("https://google.co.in/maps")
print("Accessing Google Map Services .... ")

# Signing in:
while True:
    try:
        sign_in = driver.find_element_by_id('gb_70')
        break
    except Exception:
        time.sleep(0.1)
        continue
sign_in.click()

# Entering credentials:
while True:
    try:
        username = driver.find_element_by_id('identifierId')
        username.send_keys("sudhanshu1k")

        next_button = driver.find_element_by_xpath('//*[@id="identifierNext"]/content/span')
        break
    except Exception:
        time.sleep(0.1)
        continue
next_button.click()

# Entering Password:
while True:
    try:
        password = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
        password.send_keys("krinkhold13")

        after_pass = driver.find_element_by_xpath('//*[@id="passwordNext"]')
        break
    except Exception:
        time.sleep(0.1)
        continue
after_pass.click()

print("Determining the co-ordinates .... ")
# Getting the location:
while True:
    try:
        location_button = driver.find_element_by_xpath('//*[@id="widget-mylocation"]')
        break
    except Exception:
        time.sleep(0.1)
        continue
location_button.click()

print("Trangulating the location .... ")
# Zooming in:
while True:
    try:
        zoom_button = driver.find_element_by_xpath('//*[@id="widget-zoom-in"]')
        break
    except Exception:
        time.sleep(0.1)
        continue
        
for i in range(5):
    zoom_button.click()
    time.sleep(2)

print(driver.current_url)

# Getting info:
url_strings = repr(driver.current_url).split("@")
url_location = url_strings[1].split(",")
url_lat = float(url_location[0])
url_long = float(url_location[1])
print("LAT : {0}".format(url_lat))
print("LONG : {0}".format(url_long))

# Configuring the PubNub connection:
pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-29e0c45e-724c-42ba-be7b-cb156fc74a03"
pnconfig.subscribe_key = "sub-c-f739ed7a-2afb-11e9-8c30-16f8bea0bbad"
pnconfig.ssl = False
pubnub = PubNub(pnconfig)

# Listener to handle the subscription:
my_listener = SubscribeListener()
pubnub.add_listener(my_listener)

# Subscribing to the channel:
pubnub.subscribe().channels('ESIoT').execute()
my_listener.wait_for_connect()
print('Subscriber Configured !')
print('_______________________')

i = 1

fig = plt.figure()
plt.xlim(-20, 20)
plt.ylim(-20, 20)
plt.axhline(y=0, color='r')
plt.axvline(x=0, color='r')

plt.xlabel("Distance Units")
plt.ylabel("Distance Units")
plt.title("Trajectory of the other Device.")
xdata, ydata = [], []
graph, = plt.plot([], [], '-')


def animate(x, y):
    xdata.append(x)
    ydata.append(y)
    graph.set_data(xdata, ydata)
    return graph


# Making the script run continuously
while True:

    print("Waiting for the other device .... ")

    # Listening for messages:
    result = my_listener.wait_for_message_on('ESIoT')
    print(result.message)

    result_message: str = repr(result.message)

    # Waiting for connection:
    if result.message == str("Connected !"):
        print("\nRemote device calliberated and ready for transmission !")
        print("_______________________________________________________")

    else:

        # Filtering the lat-long from received message:
        result_loc = result_message.split('_')
        result_lat = float(result_loc[0][1:])
        result_long = float(result_loc[1][:-1])
        print("Received LAT : {0}".format(result_lat))
        print("Received LONG : {0}".format(result_long))
        print("MY LAT - LONG : {0} , {1}".format(url_lat, url_long))
        print("______")

        # Calculating relative co-ordinates:
        relative_lat = result_lat - url_lat
        relative_long = result_long - url_long

        latdata.append(relative_lat)
        longdata.append(relative_long)

        # Calculating distance between two points using 'Haversine Formula'.
        # This formula calculates the distance "As a crow flies", which is the
        # shortest distance between two points on a spheroid.
        # HAVERSINE FORMULA ->
        # a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)      ---Angle.
        # c = 2 ⋅ atan2( √a, √(1−a) )                       ---Calculation.
        # d = Radius ⋅ c                                    ---Distance.
        #
        # [ Here, φ is latitude, λ is longitude ]

        a = math.pow(math.sin((relative_lat/2) * p), 2) + \
            math.cos(result_lat * p) * math.cos(url_lat) * math.pow(math.sin((relative_long / 2) * p), 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        d = radius * c

        print("Distance = {0} meters.".format(d))
        print("_______________________")

        ani = FuncAnimation(fig, animate(i, i+1), frames=10, interval=200)
        i = i + 1
        plt.draw()
        plt.pause(0.1)

