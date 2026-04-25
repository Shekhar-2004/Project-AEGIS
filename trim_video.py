"""
trim_video.py — Trim a video using start and end timestamps.

Usage:
    python trim_video.py <input_file> <start_time> <end_time> [output_file]

Time formats accepted:
    HH:MM:SS       e.g.  0:01:30
    MM:SS          e.g.  1:30
    Seconds only   e.g.  90

Examples:
    python trim_video.py movie.mp4 0:30 1:45
    python trim_video.py movie.mp4 00:01:00 00:03:30 trimmed.mp4
    python trim_video.py lecture.mkv 90 270

Requirements:
    pip install ffmpeg-python
    ffmpeg must be installed on your system:
        Ubuntu/Debian : sudo apt install ffmpeg
        macOS         : brew install ffmpeg
        Windows       : https://ffmpeg.org/download.html
"""

import argparse
import os
import sys

try:
    import ffmpeg
except ImportError:
    print("Error: ffmpeg-python is not installed.")
    print("Install it with:  pip install ffmpeg-python")
    sys.exit(1)


def parse_time(time_str: str) -> float:
    """Convert a time string (HH:MM:SS, MM:SS, or raw seconds) to seconds (float)."""
    time_str = time_str.strip()
    parts = time_str.split(":")
    try:
        if len(parts) == 1:
            return float(parts[0])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        else:
            raise ValueError
    except ValueError:
        print(f"Error: Could not parse time '{time_str}'. Use HH:MM:SS, MM:SS, or seconds.")
        sys.exit(1)


def build_output_path(input_path: str, start: str, end: str) -> str:
    """Generate a default output filename based on the input file."""
    base, ext = os.path.splitext(input_path)
    safe_start = start.replace(":", "-")
    safe_end = end.replace(":", "-")
    return f"{base}_trim_{safe_start}_to_{safe_end}{ext}"


def trim_video(input_path: str, start_str: str, end_str: str, output_path: str) -> None:
    """Trim the video from start_str to end_str and save to output_path."""

    if not os.path.isfile(input_path):
        print(f"Error: Input file not found: '{input_path}'")
        sys.exit(1)

    start_sec = parse_time(start_str)
    end_sec = parse_time(end_str)

    if end_sec <= start_sec:
        print(f"Error: End time ({end_str}) must be greater than start time ({start_str}).")
        sys.exit(1)

    duration = end_sec - start_sec

    print(f"Input   : {input_path}")
    print(f"Start   : {start_str}  ({start_sec:.2f}s)")
    print(f"End     : {end_str}  ({end_sec:.2f}s)")
    print(f"Duration: {duration:.2f}s")
    print(f"Output  : {output_path}")
    print("Trimming...")

    try:
        (
            ffmpeg
            .input(input_path, ss=start_sec, t=duration)
            .output(output_path, c="copy")   # stream-copy = fast, no re-encoding
            .overwrite_output()
            .run(quiet=True)
        )
        print(f"\nDone! Trimmed video saved to: {output_path}")
    except ffmpeg.Error as e:
        print("\nffmpeg error:")
        print(e.stderr.decode() if e.stderr else str(e))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Trim a video file between a start and end timestamp."
    )
    parser.add_argument("input",   help="Path to the input video file")
    parser.add_argument("start",   help="Start time (HH:MM:SS, MM:SS, or seconds)")
    parser.add_argument("end",     help="End time   (HH:MM:SS, MM:SS, or seconds)")
    parser.add_argument("output",  nargs="?", default=None,
                        help="Output file path (optional; auto-generated if omitted)")

    args = parser.parse_args()

    output_path = args.output or build_output_path(args.input, args.start, args.end)
    trim_video(args.input, args.start, args.end, output_path)


if __name__ == "__main__":
    main()