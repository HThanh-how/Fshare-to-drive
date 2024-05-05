import os
import subprocess
import json

# Directory to save subtitles
subtitle_dir = "C:/Subtitles"

current_dir = os.getcwd()

# Path to mkvmerge tool
mkvinfo_path = "C:/mkvtoolnix/mkvinfo.exe"

# Iterate over MKV files in current directory
print("Runningg...\n")
for filename in os.listdir(current_dir):
    if filename.endswith(".mkv"):
        isContainSubtitles = False
        # Split video name from file name
        video_name, ext = os.path.splitext(filename)
        print("Extracting subtitles for", video_name)
        # Get the list of subtitle tracks
        # mkvmerge [global options] {-o out} [options1] {file1} [[options2] {file2}] [@options-file.json]
        command = [mkvinfo_path, os.path.join(current_dir, filename)]
        # print('[+] COMMAND: ', command)
        result = subprocess.run(command, capture_output=True, text=True)
        # print('[+] RESULT:', result.stdout)
        lines = result.stdout.splitlines()
        # Split the output into sections for each track
        tracks = result.stdout.split("| + Track")
        # print('[+] TRACKS:', tracks)
        # print('[+] TRACKS TEST:', tracks[1])
        track_info_list = []
        lang_name_map = {}
        # Skip the first section, which doesn't correspond to a track
        with open('report.txt', 'w') as f:
            # Process each track
            for track in tracks[1:]:
                # Extract track information
                track_number = track.split("Track number: ")[1].split(" ")[0]
                track_type = track.split("Track type: ")[1].split("\n")[0]
                codec_id = track.split("Codec ID: ")[1].split("\n")[0]

                # Handle missing language or name
                language = track.split("Language: ")[1].split("\n")[0] if "Language: " in track else "und"
                name = track.split("Name: ")[1].split("\n")[0] if "Name: " in track else "und"

                # write to file
                f.write(f"Track number: {track_number}\n")
                f.write(f"Track type: {track_type}\n")
                f.write(f"Codec ID: {codec_id}\n")
                f.write(f"Language: {language}\n")
                f.write(f"Name: {name}\n")
                f.write("\n")

                # Add track information to list
                track_info_list.append({
                    "track_number": track_number,
                    "track_type": track_type,
                    "codec_id": codec_id,
                    "language": language,
                    "name": name
                })

                # Create a language-name map for tracks with full language and name
                lang_name_map = {info["language"]: info["name"] for info in track_info_list if
                                 info["language"] != "und" and info["name"] != "und"}
                # print(track_type,"\n")
                if track_type== "subtitles":
                    isContainSubtitles = True
                    # print('[+] COMMAND:', command, track_number)
                    subtitle_file = os.path.join(subtitle_dir, f"{video_name}_{language}.srt")

                    # Check if subtitle file already exists
                    if not os.path.exists(subtitle_file):
                        # print('[+] SUBTITLE FILE:', subtitle_file)
                        # Command to extract subtitles
                        track_id = str(int(track_number) - 1) if int(track_number) > 0 else str(track_number)
                        command = ["C:/mkvtoolnix/mkvextract.exe", "tracks", os.path.join(current_dir, filename), f"{track_id}:{subtitle_file}"]
                        subtitle_file = os.path.join(subtitle_dir, f"{video_name}_{language}.srt")
                        # Run command
                        subprocess.run(command, check=True)

                        print("\n")
                        print(f"Extracted subtitles for {video_name} - {language} successfully!")

                    else:
                        print(f"Subtitles for {video_name} - {language} already exist!")

        if not isContainSubtitles:       print(f"{video_name} do not contain subtitles ")
        print("\n")

        # # Update 'und' languages and names in the list
        # for info in track_info_list:
        #     if info["language"] == "und" and info["name"] in lang_name_map:
        #         info["language"] = lang_name_map[info["name"]]
        #     if info["name"] == "und" and info["language"] in lang_name_map.values():
        #         info["name"] = next(key for key, value in lang_name_map.items() if value == info["language"])

        # # Store the list in a file
        # with open('track_info.json', 'w') as f:
        #     json.dump(track_info_list, f)