def get_video_metadata(path: str):
    # Dev stub: return a minimal metadata dict
    return {"duration": 0, "codec": None}
from moviepy.editor import VideoFileClip
from app.models import VideoMetadata


def get_video_metadata(file_path: str) -> VideoMetadata:
    clip = VideoFileClip(file_path)
    metadata = VideoMetadata(
        duration_s=clip.duration,
        fps=clip.fps,
        resolution=[int(clip.w), int(clip.h)],
    )
    clip.reader.close()
    if clip.audio:
        clip.audio.reader.close_proc()
    return metadata
