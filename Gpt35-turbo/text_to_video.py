import os
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureTextCompletion
from myPlugins.audioPlugin.audioPlugin import AudioPlugin
from myPlugins.imagePlugin.imagePlugin import ImagePlugin
from myPlugins.videoPlugin.videoPlugin import VideoPlugin
from dotenv import load_dotenv
import time

def semanticFunctions(kernel, skills_directory, skill_name,input):
    functions = kernel.import_semantic_skill_from_directory(skills_directory, "myPlugins")
    summarizeFunction = functions[skill_name]
    return summarizeFunction(input)
    

def nativeFunctions(kernel, context, plugin_class,skill_name, function_name):
    native_plugin = kernel.import_skill(plugin_class, skill_name)
    function = native_plugin[function_name]    
    function.invoke(context=context) 

def main():
    
    #Load environment variables from .env file
    load_dotenv()

    # Create a new kernel
    kernel = sk.Kernel()
    context = kernel.create_new_context()

    # Configure AI service used by the kernel
    deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()

    # Add the AI service to the kernel
    kernel.add_text_completion_service("dv", AzureTextCompletion(deployment, endpoint, api_key))

    # Getting user input
    user_input = input("Enter your content:")

    # Generating summary
    skills_directory = "."
    print("Generating the summary............... ")
    start = time.time()
    result_sum = semanticFunctions(kernel, skills_directory,"summarizePlugin",user_input).result.split('\n')[0]
    print("Time taken(secs): ", time.time() - start)

    # Generating audio
    print("Creating audio.................")    
    context["content"] = result_sum
    context["speech_key"] = os.getenv("SPEECH_KEY")
    context["speech_region"] = os.getenv("SPEECH_REGION")
    start = time.time()
    nativeFunctions(kernel, context, AudioPlugin(),"audio_plugin","create_audio_file")
    print("Time taken(secs): ", time.time() - start)

    # Generating image prompts
    print("Creating Dall-e prompts.................")
    start = time.time()
    image_prompts = semanticFunctions(kernel,skills_directory,"promptPlugin",result_sum).result.split('\n\n')[0].split("<")[0].split('\n')
    print("Time taken(secs): ", time.time() - start)

    # Generating images
    print("Creating images.................")
    context["prompts"] = image_prompts
    context["api_base"] = os.getenv("DALLE_API_BASE")
    context["api_key"] = os.getenv("DALLE_API_KEY")
    context["api_version"] = os.getenv("DALLE_API_VERSION")
    start = time.time()
    nativeFunctions(kernel, context, ImagePlugin(),"image_plugin","create_image_files")
    print("Time taken(secs): ", time.time() - start)
    
    # Generating video
    print("Creating video.................")
    start = time.time()
    nativeFunctions(kernel, context, VideoPlugin(),"video_plugin","create_video_file")
    print("Time taken(secs): ", time.time() - start)
  


if __name__ == "__main__":
    start = time.time()
    main()
    print("Time taken Overall(mins): ", (time.time() - start)/60)