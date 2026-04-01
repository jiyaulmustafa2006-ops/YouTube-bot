from moviepy.editor import *
import os
import requests
from logger import logger

def create_shorts(audio_path, video_urls, output_path, subtitles=None):
    video_clips = []
    for i, url in enumerate(video_urls[:3]):
        local_file = f"temp_video_{i}.mp4"
        try:
            r = requests.get(url, stream=True)
            with open(local_file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            clip = VideoFileClip(local_file)
            video_clips.append(clip)
        except Exception as e:
            logger.warning(f"Failed to download video {url}: {e}")

    if not video_clips:
        video_clips = [ColorClip(size=(1080,1920), color=(0,0,0), duration=60)]

    final_video = concatenate_videoclips(video_clips, method="compose")
    audio = AudioFileClip(audio_path)
    final_video = final_video.set_audio(audio)
    final_video = final_video.set_duration(audio.duration)

    final_video = final_video.resize(height=1920).crop(x_center=final_video.w/2, y_center=final_video.h/2, width=1080, height=1920)

    if subtitles:
        txt_clip = TextClip(subtitles, fontsize=24, color='white', font='Arial', stroke_color='black', stroke_width=1)
        txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(audio.duration)
        final_video = CompositeVideoClip([final_video, txt_clip])

    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24)

    for clip in video_clips:
        clip.close()
    for i in range(len(video_urls[:3])):
        file = f"temp_video_{i}.mp4"
        if os.path.exists(file):
            os.remove(file)
    logger.info(f"Shorts created: {output_path}")

def create_long_video(audio_path, video_urls, output_path, subtitles=None):
    video_clips = []
    for i, url in enumerate(video_urls[:5]):
        local_file = f"temp_video_{i}.mp4"
        try:
            r = requests.get(url, stream=True)
            with open(local_file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            clip = VideoFileClip(local_file)
            video_clips.append(clip)
        except Exception as e:
            logger.warning(f"Failed to download video {url}: {e}")

    if not video_clips:
        video_clips = [ColorClip(size=(1920,1080), color=(0,0,0), duration=60)]

    final_video = concatenate_videoclips(video_clips, method="compose")
    audio = AudioFileClip(audio_path)
    final_video = final_video.set_audio(audio)
    final_video = final_video.set_duration(audio.duration)

    final_video = final_video.resize(height=1080).crop(x_center=final_video.w/2, y_center=final_video.h/2, width=1920, height=1080)

    if subtitles:
        txt_clip = TextClip(subtitles, fontsize=24, color='white', font='Arial', stroke_color='black', stroke_width=1)
        txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(audio.duration)
        final_video = CompositeVideoClip([final_video, txt_clip])

    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24)

    for clip in video_clips:
        clip.close()
    for i in range(len(video_urls[:5])):
        file = f"temp_video_{i}.mp4"
        if os.path.exists(file):
            os.remove(file)
    logger.info(f"Long video created: {output_path}")
