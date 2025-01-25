import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter


class Youtuber:
    """
    A class to fetch and format YouTube video transcripts.
    """

    def get_transcript_by_url(self, video_url: str) -> str:
        """
        Fetches the transcript of a YouTube video using its URL.

        Args:
            video_url (str): The URL of the YouTube video.

        Returns:
            str: The formatted transcript of the video or an error message.
        """

        try:
            # Extract the video ID from the URL using regex
            video_id = re.search(r"v=([a-zA-Z0-9_-]+)", video_url).group(1)
            return self.get_transcript_by_id(video_id)
        
        except Exception as e:
            return f"Error fetching transcript: {e}"

    def get_transcript_by_id(self, video_id: str) -> str:
        """
        Fetches the transcript of a YouTube video using its video ID.

        Args:
            video_id (str): The ID of the YouTube video.

        Returns:
            str: The formatted transcript of the video or an error message.
        """
        
        try:
            print(f"Fetching transcript for video ID: {video_id}")

            # Fetch transcript using youtube-transcript-api
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            formatter = TextFormatter()
            formatted_transcript = formatter.format_transcript(transcript)

            print("Transcript retrieved successfully!")
            return formatted_transcript
        
        except Exception as e:
            return f"Error fetching transcript: {e}"

if __name__ == "__main__":
    # Input YouTube video URL
    video_url = input("Enter the YouTube video URL: ")

    # Fetch and print the transcript
    youtuber = Youtuber()
    transcript = youtuber.get_transcript_by_url(video_url)
    print("\nTranscript:\n")
    print(transcript)
