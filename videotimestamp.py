from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import re
from datetime import datetime
from datetime import timedelta

def videotimestamp(video_file_path):

    metadata_string = metadata(video_file_path)
    start = "Creation date: "
    end = "\n"
    time_string = re.search('%s(.*)%s'%(start, end), metadata_string).group(1)
    #convert time_string to datetime object
    video_creation_datetime = datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')

    return video_creation_datetime

def videoendtime(video_file_path):

    start_time = videotimestamp(video_file_path)
    duration = duration_seconds(video_file_path)

    end_time = start_time + timedelta(seconds = duration)
    
    return end_time

def metadata(video_file_path):
    "returns a string of metadata from given video"

    #extract metadata from video file
    parser = createParser(video_file_path)
    metadata = extractMetadata(parser)

    #extract creation date from metadata
    metadata_string = str(metadata)

    return metadata_string

# helper functions -------------------------------------------------------------------------

def duration_string(video_file_path):

    metadata_string = metadata(video_file_path)
    start = "Duration: "
    end = "\n"
    duration_string = re.search('%s(.*)%s'%(start, end), metadata_string).group(1)

    return duration_string

def duration_seconds(video_file_path):

    x = duration_string(video_file_path)

    start_min = ""
    end_min = " min"

    try:
        minutes = int(re.search('%s(.*)%s'%(start_min, end_min), x).group(1))
    except:
        minutes = 0

    try:
        start_sec = "min "
        end_sec = " sec"
        seconds = int(re.search('%s(.*)%s'%(start_sec, end_sec), x).group(1))
    except:
        start_sec = ""
        end_sec = " sec"
        seconds = int(re.search('%s(.*)%s'%(start_sec, end_sec), x).group(1))

    return int(minutes*60 + seconds)
    
