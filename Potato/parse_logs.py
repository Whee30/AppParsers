import os

path_to_logs = "./potato_logs/logs"

video_flag = "videoId = "

id_holder = []

with open("output.txt", "w") as output_file:
    for each_file in os.listdir(path_to_logs):
        file_path = os.path.join(path_to_logs, each_file)
        with open(file_path, "r", encoding="utf-8", errors="ignore") as log_file:
            for line in log_file:
                if video_flag in line:
                    last_19 = line[-20:].strip()
                    hex_19 = hex(int(last_19))[2:]
                    id_holder.append(hex_19)
                    output_file.write(f"In {each_file}, {line}")

with open("id_list.csv", "w") as id_file:
    for item in id_holder:
        id_file.write(item + "\n") 
                