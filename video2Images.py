import cv2
import os
import argparse
import numpy as np


def calculate_sharpness(frame):
    """Calculate the sharpness of a frame using the Laplacian method."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var


def estimate_motion(prev_gray, curr_gray):
    """Estimate the motion between two frames using optical flow."""
    flow = cv2.calcOpticalFlowFarneback(
        prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0
    )
    motion = np.mean(np.abs(flow))
    return motion


def capture_best_frames(video_path, output_folder, num_images, sharpness_threshold, motion_threshold):
    print("Starting frame capture process...")
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames in video: {total_frames}")

    frames_to_capture = []
    prev_frame_gray = None

    for frame_number in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            print(f"Finished processing frames. Total frames processed: {frame_number}")
            break

        # Convert current frame to grayscale
        curr_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sharpness = calculate_sharpness(frame)

        # Calculate motion only if it's not the first frame
        if prev_frame_gray is not None:
            motion = estimate_motion(prev_frame_gray, curr_frame_gray)
        else:
            motion = 0

            # Alternate between two different formats based on the frame number for better readability
        if frame_number % 2 == 0:
            print(
                f"\033[1;37;40mFrame {frame_number}: Sharpness={sharpness:.2f}, Motion={motion:.2f}\033[0m"
            )
        else:
            print(
                f"\033[1;30;47mFrame {frame_number}: Sharpness={sharpness:.2f}, Motion={motion:.2f}\033[0m"
            )

        # Only append frames that meet the sharpness and motion thresholds
        if sharpness > sharpness_threshold and motion < motion_threshold:
            frames_to_capture.append((frame_number, sharpness, motion))

        # Update previous frame
        prev_frame_gray = curr_frame_gray

    cap.release()

    if not frames_to_capture:
        print("No frames met the criteria. Try adjusting the thresholds.")
        return

    print(f"\nTotal frames meeting criteria: {len(frames_to_capture)}")

    # Sort by sharpness (desc) and then by motion (asc)
    frames_to_capture.sort(key=lambda x: (-x[1], x[2], x[0]))

    # Select evenly spaced frames from the sorted list
    selected_frames = []
    frame_interval = max(1, len(frames_to_capture) // num_images)
    for i in range(0, len(frames_to_capture), frame_interval):
        if len(selected_frames) >= num_images:
            break
        selected_frames.append(frames_to_capture[i])

    print(f"Selected {len(selected_frames)} frames for extraction.")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save selected frames
    cap = cv2.VideoCapture(video_path)
    for frame_index, _, _ in selected_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = cap.read()
        if ret:
            output_path = os.path.join(output_folder, f"frame_{frame_index:04d}.jpg")
            cv2.imwrite(output_path, frame)
            print(f"\nCaptured frame {frame_index} as {output_path}")
    cap.release()

    print("Frame capture process completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract the best frames from a video for photogrammetry, minimizing blur and maximizing overlap."
    )
    parser.add_argument("video", help="Path to the video file.")
    parser.add_argument("output_folder", help="Directory to save the extracted images.")
    parser.add_argument(
        "num_images", type=int, help="Number of high-quality images to extract."
    )
    parser.add_argument(
        "--sharpness_threshold",
        type=float,
        default=100.0,
        help="Sharpness threshold for selecting frames. Default is 100.0.",
    )
    parser.add_argument(
        "--motion_threshold",
        type=float,
        default=5.0,
        help="Motion threshold for selecting frames. Default is 5.0.",
    )

    args = parser.parse_args()

    capture_best_frames(
        args.video,
        args.output_folder,
        args.num_images,
        args.sharpness_threshold,
        args.motion_threshold,
    )
