import azure.cognitiveservices.speech as speechsdk
from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter,
)
from semantic_kernel.orchestration.sk_context import SKContext


class AudioPlugin:
    @sk_function(
        description="Creates a audio file with the given content",
        name="create_audio_file",
        input_description="The content to be converted to audio",
    )
    @sk_function_context_parameter(
        name="content",
        description="The content to be converted to audio",
    )
    @sk_function_context_parameter(
        name="speech_key",
        description="speech_key",
    )
    @sk_function_context_parameter(
        name="speech_region",
        description="speech_region",
    )
    def create_audio_file(self, context: SKContext):        
        speech_config = speechsdk.SpeechConfig(subscription=context["speech_key"], region=context["speech_region"])
        content = context["content"]
        filename = "Audio/audio.mp4"
        audio_config = speechsdk.AudioConfig(filename=filename)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = speech_synthesizer.speak_text_async(content).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"Audio saved to {filename}")
        else:
            print(f"Error: {result.error_details}")
        print("Audio file created.....")
        
