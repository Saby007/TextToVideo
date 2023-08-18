from moviepy.editor import *
from semantic_kernel.skill_definition import (
    sk_function    
)
from semantic_kernel.orchestration.sk_context import SKContext


class VideoPlugin:
    @sk_function(
        description="Creates images with the given prompts",
        name="create_video_file",
        input_description="The content to be converted to images",
    )
    def create_video_file(self, context: SKContext):
        images = []
        for i in range(1,11):
            images.append("Images/file" + str(i) + ".jpg")
        audio = "Audio/audio.mp4"
        output = "Video/video.mp4"
        self.create_video(images, audio, output)
        print("Video created.....")

    def create_video(self,images, audio, output):
        clips = [ImageClip(m).resize(height=1024).set_duration(3) for m in images]
        concat_clip = concatenate_videoclips(clips, method="compose")
        audio_clip = AudioFileClip(audio)
        final_clip = concat_clip.set_audio(audio_clip)
        final_clip.write_videofile(output, fps=20)