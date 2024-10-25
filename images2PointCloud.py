import os
import subprocess
import argparse
import time


def run_meshroom(input_folder, output_folder):
    meshroom_batch_executable = (
        "/home/gal/Documents/Final Project/Meshroom/meshroom_batch"
    )

    print("Starting Meshroom processing...")
    print(f"Input folder: {input_folder}")
    print(f"Output folder: {output_folder}")

    process = subprocess.Popen(
        [meshroom_batch_executable, "--input", input_folder, "--output", output_folder],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    while True:
        output = process.stdout.readline()
        if process.poll() is not None and output == b"":
            break
        if output:
            print(f"[Meshroom] {output.strip().decode('utf-8')}")

    process.wait()

    if process.returncode == 0:
        print("Meshroom processing completed successfully.")
    else:
        print("Meshroom processing encountered an error.")
        _, error_output = process.communicate()
        print(f"Error details: {error_output.decode('utf-8')}")

    print("Finished processing.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process images with Meshroom to generate a point cloud."
    )
    parser.add_argument("input_folder", help="Directory containing the input images.")
    parser.add_argument(
        "output_folder", help="Directory to save the output point cloud."
    )

    args = parser.parse_args()

    if not os.path.exists(args.output_folder):
        print(f"Output folder '{args.output_folder}' does not exist. Creating it now.")
        os.makedirs(args.output_folder)

    print("Preparing to run Meshroom...")
    start_time = time.time()

    run_meshroom(args.input_folder, args.output_folder)

    end_time = time.time()
    print(f"Total processing time: {end_time - start_time:.2f} seconds")
