import psutil
import time

CARBON_INTENSITY = 700

def estimate_power(cpu, ram):

    base_power = 20
    cpu_power = cpu * 0.8
    ram_power = ram * 0.05

    return base_power + cpu_power + ram_power

print("\nLive Digital Carbon Monitor\n")

while True:

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    power = estimate_power(cpu, ram)

    energy_per_minute = power / 60

    co2 = (energy_per_minute/1000) * CARBON_INTENSITY

    print("CPU:", cpu,"%")
    print("RAM:", ram,"%")
    print("Estimated Power:", round(power,2),"W")
    print("CO2 per minute:", round(co2,3),"g")

    time.sleep(3)