# Smart Traffic Management System for Bhubaneswar
import random
import time
from datetime import datetime
def read_traffic_cameras(intersection_id):
    vehicle_count = random.randint(5, 100)
    traffic_density = round(random.uniform(0.1, 0.95), 2)
    return vehicle_count, traffic_density

def read_inductive_loops(intersection_id):
    avg_speed = round(random.uniform(5, 60), 1)
    flow_rate = round(random.uniform(5, 120), 0)
    return avg_speed, flow_rate
def read_acoustic_sensors(intersection_id):
    emergency_vehicle_present = random.random() < 0.05  
    noise_level = round(random.uniform(1, 10), 1)
    return emergency_vehicle_present, noise_level
def analyze_traffic_conditions(intersection_id, vehicle_count, density, speed, flow_rate, emergency_vehicle):
    congestion_score = 0
    if vehicle_count < 20:
        congestion_score += 0
    elif vehicle_count < 40:
        congestion_score += 1
    elif vehicle_count < 60:
        congestion_score += 2
    else:
        congestion_score += 3
    congestion_score += int(density * 5)
    if speed < 10:
        congestion_score += 3
    elif speed < 20:
        congestion_score += 2
    elif speed < 30:
        congestion_score += 1
   if congestion_score < 3:
        congestion_level = "LOW"
    elif congestion_score < 6:
        congestion_level = "MODERATE"
    elif congestion_score < 9:
        congestion_level = "HIGH"
    else:
        congestion_level = "SEVERE"
   if emergency_vehicle:
        green_time = 45 
        congestion_level = "EMERGENCY VEHICLE DETECTED"
    elif congestion_level == "LOW":
        green_time = 20
    elif congestion_level == "MODERATE":
        green_time = 30
    elif congestion_level == "HIGH":
        green_time = 40
    else:  
        green_time = 45  
    return congestion_level, green_time
def control_traffic_signal(intersection_id, direction, green_time):
    print(f"Setting intersection {intersection_id} {direction} signal to GREEN for {green_time} seconds")
    time.sleep(1)
    print(f"Intersection {intersection_id} {direction} signal returned to RED")
    return True
def update_message_sign(intersection_id, message):
    print(f"VMS near intersection {intersection_id} now displaying: '{message}'")
    return True
def store_traffic_data(timestamp, intersection_id, direction, vehicle_count, density, 
                      speed, flow_rate, congestion_level, green_time):
    with open("traffic_data.csv", "a") as file:
        file.write(f"{timestamp},{intersection_id},{direction},{vehicle_count},{density}," +
                   f"{speed},{flow_rate},{congestion_level},{green_time}\n")
def run_traffic_management_system():
    print("Starting Smart Traffic Management System for Bhubaneswar...")
    print("----------------------------------------------------------")
    with open("traffic_data.csv", "w") as file:
        file.write("timestamp,intersection_id,direction,vehicle_count,density," +
                  "speed,flow_rate,congestion_level,green_time\n")
    intersections = {
        "INT001": {
            "name": "Jaydev Vihar Square", 
            "directions": ["North-South", "East-West"]
        },
        "INT002": {
            "name": "Acharya Vihar Square", 
            "directions": ["North-South", "East-West"]
        },
        "INT003": {
            "name": "Rasulgarh Square", 
            "directions": ["North-South", "East-West"]
        },
        "INT004": {
            "name": "Master Canteen Square", 
            "directions": ["North-South", "East-West"]
        }
    }
    
    try:
        for cycle in range(1, 6):
            cycle_time = datetime.now()
            print(f"\n--- Traffic Cycle {cycle} - {cycle_time.strftime('%Y-%m-%d %H:%M:%S')} ---")
            
            for intersection_id, intersection_info in intersections.items():
                print(f"\nMonitoring {intersection_info['name']} ({intersection_id}):")
                
                for direction in intersection_info['directions']:
                    vehicle_count, traffic_density = read_traffic_cameras(intersection_id)
                    avg_speed, flow_rate = read_inductive_loops(intersection_id)
                    emergency_vehicle, noise_level = read_acoustic_sensors(intersection_id)
                    congestion_level, green_time = analyze_traffic_conditions(
                        intersection_id, vehicle_count, traffic_density, 
                        avg_speed, flow_rate, emergency_vehicle
                    )
                    print(f"  {direction} Direction:")
                    print(f"    Vehicle Count: {vehicle_count}, Density: {traffic_density}")
                    print(f"    Average Speed: {avg_speed} km/h, Flow Rate: {flow_rate} vehicles/min")
                    print(f"    Congestion Level: {congestion_level}")
                    control_traffic_signal(intersection_id, direction, green_time)
                    if congestion_level in ["HIGH", "SEVERE"]:
                        message = f"Heavy traffic at {intersection_info['name']}. Consider alternate routes."
                        update_message_sign(intersection_id, message)
                    elif emergency_vehicle:
                        message = "EMERGENCY VEHICLE APPROACHING. Please clear the way."
                        update_message_sign(intersection_id, message)
                    timestamp = cycle_time.strftime('%Y-%m-%d %H:%M:%S')
                    store_traffic_data(
                        timestamp, intersection_id, direction, vehicle_count, 
                        traffic_density, avg_speed, flow_rate, congestion_level, green_time
                    )
            print("\nWaiting for next traffic monitoring cycle...")
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\nSystem stopped by user")
    
    print("Smart Traffic Management System shutdown complete")
    print("Traffic data has been saved to traffic_data.csv for analysis")
if __name__ == "__main__":
    run_traffic_management_system()
