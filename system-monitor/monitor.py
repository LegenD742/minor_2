import psutil
import time
import requests

DEFAULT_CARBON_INTENSITY = 820

def get_live_carbon_intensity():
    try:
        response = requests.get("https://api.ccarbonintensity.org.in/intensityi")

        data = response.json()

        intensity = data["data"][0]["intensity"]["actual"]

        return intensity

    except:
        return DEFAULT_CARBON_INTENSITY


def estimate_power(cpu, ram):

    base_power = 20
    cpu_power = cpu * 0.8
    ram_power = ram * 0.05

    return base_power + cpu_power + ram_power


print("\nLive Digital Carbon Monitor\n")

while True:

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    carbon_intensity = get_live_carbon_intensity()

    power = estimate_power(cpu, ram)

    energy_per_minute = power / 60

    co2 = (energy_per_minute/1000) * carbon_intensity
    print("currently using", carbon_intensity) 

    print("CPU:", cpu,"%")
    print("RAM:", ram,"%")
    print("Estimated Power:", round(power,2),"W")
    print("Carbon Intensity:", carbon_intensity,"gCO2/kWh")
    print("CO2 per minute:", round(co2,3),"g")

    print("----------------------------------")

    time.sleep(3)