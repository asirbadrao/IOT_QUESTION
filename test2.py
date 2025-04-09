# Smart Waste Management System for Bhubaneswar
import random
import time
from datetime import datetime
def read_ultrasonic_sensor(bin_id):
    """Simulate ultrasonic sensor reading for bin fill level (percentage)"""
    return round(random.uniform(10, 95), 1)
def read_weight_sensor(bin_id):
    """Simulate weight sensor reading (kg)"""
    return round(random.uniform(5, 90), 1)
def read_methane_sensor(bin_id):
    """Simulate methane level reading (ppm)"""
   return round(random.uniform(100, 2000), 0)
def read_temperature_sensor(bin_id):
    """Simulate temperature sensor reading (Celsius)"""
     return round(random.uniform(25, 45), 1)
def determine_bin_status(fill_level, weight, methane, temperature):
    """Determine bin status based on sensor readings"""
    status = "NORMAL" 
    if fill_level > 80 or weight > 80:
        status = "FULL"
    elif fill_level > 60 or weight > 60:
        status = "WARNING"
    if methane > 1500:
        status = "CRITICAL"
    elif temperature > 40:
        status = "WARNING" 
         return status
def generate_alerts(bin_id, status, location):
    """Generate appropriate alerts based on bin status"""
    if status == "FULL":
        print(f"ALERT: Bin {bin_id} at {location} is FULL and needs collection")
        return {"type": "collection_needed", "priority": "high"}
    elif status == "WARNING":
        print(f"NOTIFICATION: Bin {bin_id} at {location} is nearing capacity")
        return {"type": "approaching_full", "priority": "medium"}
    elif status == "CRITICAL":
        print(f"URGENT ALERT: Bin {bin_id} at {location} has dangerous conditions!")
        return {"type": "dangerous_condition", "priority": "urgent"}
    else:
        return {"type": "normal", "priority": "low"}
def optimize_collection_route(bins_data):
    """Simple route optimization based on bin statuses"""
    priority_bins = []
    warning_bins = []
    normal_bins = []
    for bin_id, data in bins_data.items():
        if data["status"] == "FULL" or data["status"] == "CRITICAL":
            priority_bins.append((bin_id, data["location"]))
        elif data["status"] == "WARNING":
            warning_bins.append((bin_id, data["location"]))
        else:
            normal_bins.append((bin_id, data["location"]))
   optimized_route = priority_bins + warning_bins  
    if optimized_route:
        print("\nOptimized Collection Route:")
        for i, (bin_id, location) in enumerate(optimized_route, 1):
            print(f"{i}. Bin {bin_id} at {location}")
    else:
        print("\nNo bins require immediate collection")   
    return optimized_route
def store_bin_data(bin_id, timestamp, fill_level, weight, methane, temperature, status):
    """Store bin data to a CSV file"""
    with open("waste_management_data.csv", "a") as file:
        file.write(f"{timestamp},{bin_id},{fill_level},{weight},{methane},{temperature},{status}\n")
def run_waste_management_system():
    """Run the smart waste management system"""
    print("Starting Smart Waste Management System for Bhubaneswar...")
    print("-------------------------------------------------------")
    with open("waste_management_data.csv", "w") as file:
        file.write("timestamp,bin_id,fill_level,weight,methane,temperature,status\n")
    bins = {
        "BIN001": {"location": "Town Hall Area"},
        "BIN002": {"location": "Ekamra Park"},
        "BIN003": {"location": "Patia Market"},
        "BIN004": {"location": "Nandankanan Road"},
        "BIN005": {"location": "Master Canteen Square"},
        "BIN006": {"location": "Kalinga Stadium"},
        "BIN007": {"location": "Saheed Nagar Market"}
    }
    try:
        for cycle in range(1, 6):
            print(f"\n--- Monitoring Cycle {cycle} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
            
            bins_data = {}
            for bin_id, bin_info in bins.items():
                fill_level = read_ultrasonic_sensor(bin_id)
                weight = read_weight_sensor(bin_id)
                methane = read_methane_sensor(bin_id)
                temperature = read_temperature_sensor(bin_id)
                status = determine_bin_status(fill_level, weight, methane, temperature)
                bins_data[bin_id] = {
                    "location": bin_info["location"],
                    "fill_level": fill_level,
                    "weight": weight,
                    "methane": methane,
                    "temperature": temperature,
                    "status": status
                }
                alert = generate_alerts(bin_id, status, bin_info["location"])
                bins_data[bin_id]["alert"] = alert
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                store_bin_data(bin_id, timestamp, fill_level, weight, methane, temperature, status)
                print(f"Bin {bin_id} at {bin_info['location']}: {status}")
                print(f"  Fill Level: {fill_level}%, Weight: {weight}kg, Methane: {methane}ppm, Temp: {temperature}°C")
            optimize_collection_route(bins_data)
            print("\nWaiting for next monitoring cycle...")
            time.sleep(3)        
    except KeyboardInterrupt:
        print("\nSystem stopped by user")
    
    print("Smart Waste Management System shutdown complete")
if __name__ == "__main__":
    run_waste_management_system()
