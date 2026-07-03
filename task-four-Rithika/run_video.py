from smart_traffic_management import TrafficManagementSystem

system = TrafficManagementSystem(dataset_csv="dataset.csv")

system.process_video(
    video_path="traffic.mp4",
    save_path="output.mp4"
)