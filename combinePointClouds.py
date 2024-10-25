import os
import subprocess
import argparse
import glob
import shutil
from datetime import datetime


def combine_meshes(mesh1, mesh2, output_dir, output_name):
    cloudcompare_cli = "CloudCompare"
    command = [cloudcompare_cli, "-O", mesh1, "-O", mesh2, "-ICP", "-MERGE_MESHES"]

    try:
        # Run the CloudCompare command
        subprocess.run(command, check=True)
        print("Meshes merged successfully.")

        # Find the merged mesh file
        merged_files = glob.glob(
            os.path.join(os.path.dirname(mesh1), "texturedMesh_MERGED*.bin")
        )
        if merged_files:
            latest_file = max(merged_files, key=os.path.getctime)
            output_path = os.path.join(output_dir, output_name)
            shutil.move(latest_file, output_path)
            print(f"Merged mesh moved to: {output_path}")
        else:
            print("No merged mesh file found.")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print("Failed to merge meshes.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Combine two meshes into one point cloud and move the result to a specified directory."
    )
    parser.add_argument("mesh1", help="Path to the first mesh file (e.g., .obj).")
    parser.add_argument("mesh2", help="Path to the second mesh file (e.g., .obj).")
    parser.add_argument(
        "output_dir", help="Directory where the merged mesh will be saved."
    )
    parser.add_argument(
        "output_name", help="New name for the merged mesh file (e.g., mergedMesh.bin)."
    )

    args = parser.parse_args()

    combine_meshes(args.mesh1, args.mesh2, args.output_dir, args.output_name)
