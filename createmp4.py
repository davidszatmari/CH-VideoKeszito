from moviepy.editor import ImageClip, VideoFileClip, CompositeVideoClip, concatenate_videoclips
from PIL import Image
import os


def resize_and_pad(image, target_size, background_color=(0, 0, 0, 0)):
    original_width, original_height = image.size
    target_width, target_height = target_size

    # Calculate the target aspect ratio
    target_aspect = target_width / target_height

    # Calculate the current aspect ratio
    original_aspect = original_width / original_height

    if original_aspect > target_aspect:
        # Image is wider than target aspect ratio
        new_width = target_width
        new_height = round(target_width / original_aspect)
    else:
        # Image is taller than target aspect ratio
        new_height = target_height
        new_width = round(target_height * original_aspect)

    # Resize the image while maintaining aspect ratio
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    # Convert the image to RGBA if not already in that mode
    if resized_image.mode != 'RGBA':
        resized_image = resized_image.convert('RGBA')

    # Create a new image with the target size and the specified background color
    new_image = Image.new("RGBA", (target_width, target_height), background_color)
    new_image.paste(resized_image, ((target_width - new_width) // 2, (target_height - new_height) // 2), resized_image)

    return new_image

def create_slideshow(image_folder, output_file, last_image_file, last_image_folder, background_video, duration_per_image=2, fade_duration=1, target_size=(1080, 1920)):
    # Get list of images
    images = sorted([img for img in os.listdir(image_folder) if img.endswith(('.png', '.jpg', '.jpeg'))])

    # Load the background video
    bg_video = VideoFileClip(background_video)

    # Create ImageClips
    clips = []
    for img in images:
        image_path = os.path.join(image_folder, img)
        # Load image with Pillow
        image = Image.open(image_path)
        # Resize and pad image
        resized_image = resize_and_pad(image, target_size)
        # Save the resized image to a temporary path
        temp_image_path = os.path.join(image_folder, f"temp_{img}.png")
        resized_image.save(temp_image_path)
        # Convert to ImageClip
        image_clip = ImageClip(temp_image_path).set_duration(duration_per_image)
        # Apply fade effect to the image clip
        faded_image_clip = image_clip.crossfadein(fade_duration).crossfadeout(fade_duration)

        # Overlay the image clip on the background video
        clip = CompositeVideoClip([bg_video.set_duration(duration_per_image), faded_image_clip.set_position("center")])
        #clip = CompositeVideoClip([bg_video.set_duration(6), faded_image_clip.set_position("center")])
        clips.append(clip)

    # Load the last image
    last_image_path = os.path.join(last_image_folder, last_image_file)
    last_image = Image.open(last_image_path)
    resized_last_image = resize_and_pad(last_image, target_size)
    temp_last_image_path = os.path.join(last_image_folder, f"temp_{last_image_file}.png")
    resized_last_image.save(temp_last_image_path)
    last_image_clip = ImageClip(temp_last_image_path).set_duration(duration_per_image)
    # Overlay the last image clip on the background video
    last_clip = CompositeVideoClip([bg_video.set_duration(duration_per_image), last_image_clip.set_position("center")])
    clips.append(last_clip)


    # Concatenate all clips
    final_clip = concatenate_videoclips(clips, method="compose")

    # Write the result to a file
    final_clip.write_videofile(output_file, fps=24,  codec="libx264", preset="ultrafast", threads=8, audio=False, bitrate="5000k",verbose=False)

    print(f'Video készen van.,"{output_file}"')
    os.system(f'explorer /select,"{output_file}"')

    # Clean up temporary images
    for img in images:
        temp_image_path = os.path.join(image_folder, f"temp_{img}.png")
        clear_image_path = os.path.join(image_folder, img)
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
            os.remove(clear_image_path)
    if os.path.exists(temp_last_image_path):
        os.remove(temp_last_image_path)

