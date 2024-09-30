#!/usr/bin/env python3
"""
Video Compression Script

This script compresses a video file without significant quality loss,
producing a smaller output file. You can specify the output file path
and format, adjust compression settings, and choose between interactive
and non-interactive modes.

Usage:
    python video_compress.py input_video.mp4 [-o /path/to/output_video.mp4] [options]

Author: [Your Name]
Date: [Date]
"""

import argparse
import subprocess
import os
import sys
import re
import time

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(description='Compress a video file without significant quality loss.')
    parser.add_argument('input_file', nargs='?', help='Path to the input video file')
    parser.add_argument('-o', '--output', help='Path to the output video file')
    parser.add_argument('--crf', type=int, default=28, help='Constant Rate Factor (quality, lower is better)')
    parser.add_argument('--preset', choices=['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'], default='medium', help='Compression speed preset')
    parser.add_argument('-i', '--interactive', action='store_true', help='Run in interactive mode')
    return parser.parse_args()

def print_message(message, status='info'):
    """
    Print a message with color and icon based on status.

    Args:
        message (str): The message to print.
        status (str): The status type ('info', 'success', 'warning', 'error')
    """
    ICONS = {
        'info': '[i]',
        'success': '[+]',
        'warning': '[!]',
        'error': '[-]'
    }
    COLORS = {
        'info': '\033[94m',    # Blue
        'success': '\033[92m', # Green
        'warning': '\033[93m', # Yellow
        'error': '\033[91m'    # Red
    }
    RESET = '\033[0m'
    icon = ICONS.get(status, '')
    color = COLORS.get(status, '')
    print(f"{color}{icon} {message}{RESET}")

def check_ffmpeg():
    """
    Check if FFmpeg is installed and available in PATH.

    Returns:
        bool: True if FFmpeg is available, False otherwise
    """
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def get_video_duration(input_file):
    """
    Get the duration of the input video file in seconds.

    Args:
        input_file (str): Path to the input video file

    Returns:
        float: Duration in seconds
    """
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                                'format=duration', '-of',
                                'default=noprint_wrappers=1:nokey=1', input_file],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)
        duration = float(result.stdout)
        return duration
    except Exception as e:
        print_message(f"Could not determine video duration: {e}", 'warning')
        return None

def compress_video(input_file, output_file, crf=28, preset='medium'):
    """
    Compress the input video file and save the output to the specified path.

    Args:
        input_file (str): Path to the input video file
        output_file (str): Path to the output video file
        crf (int): Constant Rate Factor for quality (lower is better)
        preset (str): Compression speed preset
    """
    # Check if the input file exists
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' does not exist.")

    # Get the duration of the input video
    duration = get_video_duration(input_file)

    # Construct the FFmpeg command
    command = [
        'ffmpeg',
        '-i', input_file,
        '-vcodec', 'libx265',  # Use H.265 codec for better compression
        '-crf', str(crf),      # Set the Constant Rate Factor (quality, lower is better)
        '-preset', preset,     # Set the encoding speed vs compression ratio
        '-y',                  # Overwrite output file without asking
        output_file
    ]

    print_message(f"Compressing '{input_file}' to '{output_file}'...", 'info')

    # Run the FFmpeg command and capture progress
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        total_duration = duration
        pattern = re.compile(r'time=(\d+:\d+:\d+\.\d+)')

        while True:
            line = process.stderr.readline()
            if not line:
                if process.poll() is not None:
                    break
                continue
            if 'time=' in line:
                # Extract the current time
                match = pattern.search(line)
                if match:
                    current_time_str = match.group(1)
                    current_time = time_str_to_seconds(current_time_str)
                    if total_duration:
                        progress = (current_time / total_duration) * 100
                        print_message(f"Progress: {progress:.2f}%", 'info')
            if process.poll() is not None:
                break

        process.wait()
        return_code = process.returncode
        if return_code != 0:
            raise Exception("FFmpeg encountered an error.")
    except Exception as e:
        raise e

    print_message("Compression completed successfully.", 'success')

def time_str_to_seconds(time_str):
    """
    Convert a time string of format HH:MM:SS.ms to seconds.

    Args:
        time_str (str): Time string

    Returns:
        float: Time in seconds
    """
    h, m, s = time_str.split(':')
    seconds = int(h) * 3600 + int(m) * 60 + float(s)
    return seconds

def interactive_mode():
    """
    Run the script in interactive mode, prompting the user for inputs.
    """
    print_message("Running in interactive mode.", 'info')
    input_file = input("Please enter the path to your input video file: ").strip()
    while not os.path.isfile(input_file):
        print_message("File not found. Please enter a valid file path.", 'error')
        input_file = input("Please enter the path to your input video file: ").strip()

    use_default_output = input("Do you want to use the default output location? (Y/n): ").strip().lower()
    if use_default_output in ['', 'y', 'yes']:
        base_name, ext = os.path.splitext(input_file)
        output_file = f"{base_name}-cmp{ext}"
    else:
        output_file = input("Please enter the desired output file path: ").strip()

    change_format = input("Do you want to change the output format? (Y/n): ").strip().lower()
    if change_format in ['y', 'yes']:
        new_ext = input("Enter the new output format extension (e.g., .mp4, .avi): ").strip()
        if not new_ext.startswith('.'):
            new_ext = '.' + new_ext
        base_name, _ = os.path.splitext(output_file)
        output_file = f"{base_name}{new_ext}"

    adjust_quality = input("Do you want to adjust the compression quality? (Y/n): ").strip().lower()
    if adjust_quality in ['y', 'yes']:
        crf_input = input("Enter the desired CRF value (0-51, lower is better quality) [default:28]: ").strip()
        try:
            crf = int(crf_input)
            if not 0 <= crf <= 51:
                raise ValueError
        except ValueError:
            print_message("Invalid CRF value. Using default (28).", 'warning')
            crf = 28
    else:
        crf = 28

    adjust_speed = input("Do you want to adjust the compression speed? (Y/n): ").strip().lower()
    if adjust_speed in ['y', 'yes']:
        print("Available presets: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow")
        preset_input = input("Enter the desired preset [default:fast]: ").strip()
        if preset_input in ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow']:
            preset = preset_input
        else:
            print_message("Invalid preset. Using default (fast).", 'warning')
            preset = 'fast'
    else:
        preset = 'fast'

    # Build equivalent command
    equivalent_command = f"python3 {os.path.basename(sys.argv[0])} \"{input_file}\" -o \"{output_file}\" --crf {crf} --preset {preset}"

    print_message(f"Equivalent console command: {equivalent_command}", 'info')

    # Start compression
    try:
        compress_video(input_file, output_file, crf, preset)
    except Exception as e:
        print_message(f"An error occurred: {e}", 'error')
        sys.exit(1)

def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Check if FFmpeg is installed
    if not check_ffmpeg():
        print_message("FFmpeg is not installed or not found in PATH.", 'error')
        sys.exit(1)

    # If interactive mode is requested or required
    if args.interactive or not args.input_file:
        interactive_mode()
        return

    # Use arguments from command-line
    input_file = args.input_file
    output_file = args.output
    crf = args.crf
    preset = args.preset

    # Determine the output file path if not provided
    if not output_file:
        base_name, ext = os.path.splitext(input_file)
        output_file = f"{base_name}-cmp{ext}"

    # Process the video file
    try:
        compress_video(input_file, output_file, crf, preset)
    except Exception as e:
        print_message(f"An error occurred: {e}", 'error')
        sys.exit(1)

if __name__ == "__main__":
    main()

