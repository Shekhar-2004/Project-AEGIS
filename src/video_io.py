# src/video_io.py

from typing import Union
import cv2


def open_video(source: Union[int, str] = 0):
    """
    Open a video source.
    source = 0 for webcam, or file path as string.
    """
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        raise RuntimeError("Error: Could not open video source.")

    return cap

def read_frame(cap):
    """
    Read a single frame from the video capture.
    Returns: ret (bool), frame (ndarray)
    """
    ret, frame = cap.read()
    return ret, frame


def release_video(cap):
    """
    Release the video capture object.
    """
    cap.release()
