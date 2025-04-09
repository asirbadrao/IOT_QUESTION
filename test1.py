# Simple IoT-based Smart Farming System for Bhubaneswar
import random
import time
from datetime import datetime
def read_soil_moisture():
    """Simulate soil moisture sensor reading (percentage)"""
    return round(random.uniform(20, 60), 1)

def read_temperature():
    """Simulate temperature sensor reading (Celsius)"""
    return round(random.uniform(25, 38), 1)

def read_humidity():
    """Simulate humidity sensor reading (percentage)"""
    return round(random.uniform(60, 85), 1)

def read_rainfall():
    """Simulate rainfall sensor reading (mm)"""
    rain_probability = random.random()
    if rain_probability > 0.8:  
        return round(random.uniform(0.5, 10), 1)
    else:
        return 0.0
def control_irrigation(valve_id, action):
    """Control irrigation valve"""
    if action == "ON":
        print(f"Turning ON irrigation valve {valve_id}")
        return True
    else:
        print(f"Turning OFF irrigation valve {valve_id}")
        return False

def control_pump(action):
    """Control water pump"""
    if action == "ON":
        print("Turning ON water pump")
        return True
    else:
        print("Turning OFF water pump")
        return False
def analyze_farm_conditions(moisture, temp, humidity, rainfall):
    """Analyze conditions and make irrigation decision"""
    print(f"\nAnalyzing farm conditions:")
    print(f"Soil Moisture: {moisture}%")
    print(f"Temperature: {temp}°C")
    print(f"Humidity: {humidity}%")
    print(f"Rainfall: {rainfall}mm")
    if rainfall > 5.0:
        return {
            "irrigate": False,
            "reason": f"Recent rainfall detected ({rainfall}mm)"
        }
    elif moisture < 30:
        return {
            "irrigate": True,
            "duration": 20,
            "reason": f"Soil moisture too low ({moisture}%)"
        }
    elif moisture < 40 and temp > 35:
        return {
            "irrigate": True,
            "duration": 15,
            "reason": f"Soil moisture moderate ({moisture}%) but temperature high ({temp}°C)"
        }
    elif moisture < 40:
        return {
            "irrigate": True,
            "duration": 10,
            "reason": f"Soil moisture moderate ({moisture}%)"
        }
    else:
        return {
            "irrigate": False,
            "reason": f"Soil moisture adequate ({moisture}%)"
        }
def store_data(timestamp, moisture, temp, humidity, rainfall, decision):
    """Save data to a simple log file"""
    with open("farm_data.csv", "a") as file:
        file.write(f"{timestamp},{moisture},{temp},{humidity},{rainfall},{decision['irrigate']},{decision.get('duration', 0)},{decision['reason']}\n")
    print("Data saved to farm_data.csv")
def run_smart_farm_system():
    """Run the smart farm system"""
    print("Starting Smart Farm IoT System for Bhubaneswar...")
    print("--------------------------------------------------")
    with open("farm_data.csv", "w") as file:
        file.write("timestamp,moisture,temperature,humidity,rainfall,irrigate,duration,reason\n")
    
    try:
        # Simulation loop
        for cycle in range(1, 6):
            print(f"\nCycle {cycle} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("--------------------------------------------------")
            
            # 1. Read sensor data
            moisture = read_soil_moisture()
            temp = read_temperature()
            humidity = read_humidity()
            rainfall = read_rainfall()
            
            # 2. Analyze data and make decisions
            decision = analyze_farm_conditions(moisture, temp, humidity, rainfall)
            print(f"Decision: {'Irrigate' if decision['irrigate'] else 'Do not irrigate'}")
            print(f"Reason: {decision['reason']}")
            
            # 3. Take action based on decision
            if decision["irrigate"]:
                control_pump("ON")
                control_irrigation("zone1", "ON")
                print(f"Irrigating for {decision['duration']} minutes...")
                time.sleep(2)
                control_irrigation("zone1", "OFF")
                control_pump("OFF")
            store_data(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                      moisture, temp, humidity, rainfall, decision)
            time.sleep(3)    
    except KeyboardInterrupt:
        print("\nSystem stopped by user")
    print("Smart Farm System shutdown complete")
if __name__ == "__main__":
    run_smart_farm_system()
