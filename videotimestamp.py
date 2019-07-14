from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import re
from datetime import datetime

def videotimestamp(video_file_path):
    
    #video_file_path = 'Sample9.mov'

    #extract metadata from video file
    parser = createParser(video_file_path)
    metadata = extractMetadata(parser)

    #extract creation date from metadata
    metadata_string = str(metadata)
    start = "Creation date: "
    end = "\n"
    time_string = re.search('%s(.*)%s'%(start, end), metadata_string).group(1)
    #convert time_string to datetime object
    video_creation_datetime = datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')

    return video_creation_datetime

