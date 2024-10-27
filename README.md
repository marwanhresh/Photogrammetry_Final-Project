## Photogrammetry

![drone](https://github.com/user-attachments/assets/7c30efcc-6b22-4edc-9419-c85cec7e6086)

Photogrammetry uses non-contact images or scans of objects to derive three-dimensional (3D) models from surface measurements. It can be used as an analytical tool to measure the surface characteristics of objects or environments, as well as a method to display and inspect them digitally. Photogrammetry can be used to create accurate 3D models without physically removing or inspecting the object.

## Project Overview

The project focuses on creating 3D models from 2D images using photogrammetry techniques. The main components of the project include:


**cv2:**
used for image processing and computer vision The library allows working with images and videos is a Python library of OpenCV 

**CloudCompare:**

Mainly used in photogrammetry for analysis and processing of point clouds created from conversions of 2D images to 3D models
Its main use is:

**-** Processing and cleaning point clouds: noise cleaning, removing irrelevant points and focusing on the required area

**Prerequisitis**

we use the following tools:
**1)** Python
**2)** Meshroom
**3)** blender
**4)** CloudCompare 

 **Comparing models:**

 Making comparisons between point clouds or between models for example, comparing a point cloud created from new measurements with a previous cloud to detect changes


 function combine_meshes:

    Definitions:
        Receives four parameters: mesh1, mesh2 (the paths to the mesh files), output_dir (the target folder) and output_name (the new name for the combined file).
        Defines the CloudCompare command, which is a tool for processing point clouds and mesh files.

    Running the command:
        The command is compiled using a list (command) that activates CloudCompare and loads the two mesh files with the flags -ICP (registering the files using ICP - registration according to the closest points) and -MERGE_MESHES (merging the files).

The command is run using subprocess.run and when it succeeds a message appears "Meshes merged successfully."

Locating the integrated mesh file:

    After the merging is done, look for a new file with a name starting with texturedMesh_MERGED with a .bin extension, in the mesh1 directory.
    If such a file is found, the path to the destination (output_dir) and the new name (output_name) are passed, and the file is moved there using shutil.move.
    If a suitable file is not found, a message appears "No merged mesh file found."
    Error handling:
        subprocess.CalledProcessError handles errors during command execution.
        A generic Exception will handle unexpected errors and print the error.

block if name == "main":

    This is a block that allows the code to be run as a standalone script.
    The argparse module is used to read parameters from the line:
        mesh1 and mesh2 – paths to two mesh files.
        output_dir – the folder where the combined file will be saved.
        output_name – the new name of the combined file.
    Finally, the combine_meshes function is invoked with the parameters received from the user.



