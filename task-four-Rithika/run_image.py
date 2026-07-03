from smart_traffic_management import TrafficManagementSystem

system = TrafficManagementSystem(dataset_csv="dataset.csv")

signal = system.process_image(
    image_path="road.jpg",
    save_path="result.jpg"
)

print(signal)