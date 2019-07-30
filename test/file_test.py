import os


FOLDER = '/home/pi/Miac/Video/'

entries = os.listdir(FOLDER)

print("number of files ", len(entries))

print(entries[0])

entries.sort()
for entry in entries:
    print(entry)
    
print(entries[0])

print(FOLDER+entries[-1])
print(FOLDER + str(2))