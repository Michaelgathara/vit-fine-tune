import os
from glob import glob

def find_emotions(root_dir):
    emotions = set()
    # pattern: data/zenodo/IFEED_Base/Training/dia*/frame*_*_emotion.jpg
    # Actually checking recursively
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith('.jpg') and 'frame' in f:
                parts = f.replace('.jpg', '').split('_')
                if len(parts) >= 3:
                    emotion = parts[-1]
                    emotions.add(emotion)
    return emotions

print("Emotions in Training:", find_emotions("data/zenodo/IFEED_Base/Training"))
print("Emotions in Testing:", find_emotions("data/zenodo/IFEED_Base/Testing"))
