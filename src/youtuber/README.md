# Youtuber

A Python class to fetch and format YouTube video transcripts.

## Features

- Fetch transcript by video URL
- Fetch transcript by video ID

## Installation

To install the required dependencies, run:

```sh
pip install youtube-transcript-api


Usage
Fetch Transcript by URL

from youtuber import Youtuber

# Create an instance of Youtuber
youtuber = Youtuber()

# Fetch transcript by video URL
video_url = "https://www.youtube.com/watch?v=example"
transcript = youtuber.get_transcript_by_url(video_url)
print(transcript)

Fetch Transcript by ID
from youtuber import Youtuber

# Create an instance of Youtuber
youtuber = Youtuber()

# Fetch transcript by video ID
video_id = "example"
transcript = youtuber.get_transcript_by_id(video_id)
print(transcript)
Methods
get_transcript_by_url(video_url: str) -> str
Fetches the transcript of a YouTube video using its URL.

Args:
video_url (str): The URL of the YouTube video.
Returns:
str: The formatted transcript of the video or an error message.
get_transcript_by_id(video_id: str) -> str
Fetches the transcript of a YouTube video using its video ID.

Args:
video_id (str): The ID of the YouTube video.
Returns:
str: The formatted transcript of the video or an error message.

```