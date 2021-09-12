import os
import sys

with open("Observation-Camera-project.csv", "r") as inputFile, open(sys.argv[1], "w") as firstOutputFile, open(sys.argv[2], "a") as secondOutputFile:
    #   Ask the user to choose a date and trails camera
    datadict = {}
    while True:
        trailCameraLst = []
        print("Please enter date [format xx.xx.xxxx] or stop")
        date = input()
        if date == "stop":
            break;
        print("Enter trail camera number or stop")
        while True:
            trailCameraNumber = input()
            if trailCameraNumber == "stop":
                break;
            trailCameraLst.append(trailCameraNumber)
        datadict[date] = trailCameraLst

    # Ask the user to select to select category: TRAIN, TEST or UNASSIGNED
    set = None
    while set != "train" and set != "test" and set != "unassigned":
        print("Please select the kind of the set: TRAIN, TEST or UNASSIGNED")
        set = input().casefold()  # Ignore Upper case

    # Reading the CSV file and split rows
    inputFile = inputFile.read().split("\n")

    # delete the last rows in the file.
    inputFile.pop()

    # Edit the file so that we can create a CSV file in the required format. (URI,behaviour, start, end)
    for line in inputFile:
        line = line.split(",")  # split every row by ","
        date = line[0].split('/')
        for lst in datadict:
            tmpLst = lst.split(".")
            if date[0] == tmpLst[0] and date[1] == tmpLst[1] and date[2] == tmpLst[2]:
                if line[1] in datadict[lst]:
                    date = date[1] + ":" + date[0] + ":" + date[2]
                    trail_camera = line[1].zfill(2)
                    nvideo = line[2].zfill(4)
                    uri = "gs://hyrax-project/00_Camera/" + date + "/TrailCamera" + trail_camera + "/IMG_" + nvideo + ".AVI"
                    #   consider NA start and end as 0,inf
                    if line[3] == "NA" and line[4] == "" and line[5] == "":
                        line[4] = "0"
                        line[5] = "inf"
                    # arrange start and end columns
                    if line[5] == "" and line[4] != "":
                        line[5] = "inf"
                    # Write the output into a CSV file.
                    firstOutputFile.write(uri + "," + line[3].rstrip() + "," + line[4] + "," + line[5] + "\n")
    secondOutputFile.write(set.upper() + ",gs://hyrax-project/Observation-Camera-" + set + ".csv" + "\n")
os.rename(sys.argv[1], "Observation-Camera-" + set + ".csv")
