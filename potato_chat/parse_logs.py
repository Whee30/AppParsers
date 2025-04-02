import os

### In the /Documents folder, there are several application logs. Testing shows a rolling cache of 30 logfiles so far
### By putting all of the logs into oen folder and iterating through them, lines are extracted where video files are downloaded
### to the device. These logs show the timestamps when a particular video was downloaded through the application
### the video ID correlates to the filename found in /Documents/video when converted to hex.
### id_list.csv was saved as a csv so it could be imported into Cellebrite as a "watchlist" and the files could be searched for/identified in bulk.

path_to_logs = "./potato_logs"

video_flag = "videoId = "

id_holder = []

with open("output.txt", "w") as output_file:
    for each_file in os.listdir(path_to_logs):
        file_path = os.path.join(path_to_logs, each_file)
        with open(file_path, "r", encoding="utf-8", errors="ignore") as log_file:
            for line in log_file:
                if video_flag in line:
                    last_19 = line[-20:].strip()
                    print(last_19)
                    hex_19 = hex(int(last_19))[2:]
                    print(hex_19)
                    id_holder.append(hex_19)
                    output_file.write(f"In {each_file}, {line}")

with open("id_list.csv", "w") as id_file:
    for item in id_holder:
        id_file.write(item + "\n") 
                
