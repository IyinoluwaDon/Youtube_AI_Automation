import subprocess
from pathlib import Path

import imageio_ffmpeg


def burn_subtitles(
    video_path,
    subtitle_path,
    output_path
):

    ffmpeg_path = (
        imageio_ffmpeg
        .get_ffmpeg_exe()
    )

    subtitle_path = (
        str(Path(subtitle_path))
        .replace("\\", "/")
    )

    style = (
        "FontName=Arial,"
        "FontSize=8,"
        "PrimaryColour=&HFFFFFF&,"
        "OutlineColour=&H000000&,"
        "BorderStyle=1,"
        "Outline=2,"
        "Shadow=1,"
        "Bold=1,"
        "Alignment=2,"
        "MarginV=40"
    )
    command = [

        ffmpeg_path,

        "-y",

        "-i",
        str(video_path),

        "-vf",
        (
            f"subtitles='{subtitle_path}':"
            f"force_style='{style}'"
        ),

        "-c:a",
        "copy",

        str(output_path)
    ]

    print("\n========== FFMPEG COMMAND ==========\n")
    print(" ".join(command))

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    print("\n========== STDOUT ==========\n")
    print(result.stdout)

    print("\n========== STDERR ==========\n")
    print(result.stderr)

    if result.returncode != 0:

        raise Exception(
            f"\nFFmpeg Failed:\n{result.stderr}"
        )

    print(
        f"\n✅ Video Saved -> {output_path}\n"
    )

    return output_path