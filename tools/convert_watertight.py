#!/usr/bin/env python3
# convert car dataset to watertight with Manifold
import os
import argparse
from pathlib import Path
import numpy as np
import open3d as o3d
from glob import glob
import manifold
# from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def convert(filename, depth=8, export_dir='/media/data/car_mesh'):
    """Convert a triangular mesh to a watertight model."""
    filename = os.path.abspath(filename)
    model_name = Path(filename).parent.parent.stem
    extension = Path(filename).suffix
    out_filename = os.path.join(export_dir, model_name + extension)

    print("Reading", filename)
    in_mesh = o3d.io.read_triangle_mesh(filename)

    input_vertices = np.asarray(in_mesh.vertices)
    input_triangles = np.asarray(in_mesh.triangles)
    input_is_manifold = manifold.is_manifold(input_vertices, input_triangles)

    # Create the ManifoldProcessor object
    processor = manifold.Processor(input_vertices, input_triangles)

    print("Converting {} to a manifold".format(filename))
    output_vertices, output_triangles = processor.get_manifold_mesh(depth)
    output_is_manifold = manifold.is_manifold(output_vertices, output_triangles)

    print("Saving results to", out_filename)
    out_mesh = o3d.geometry.TriangleMesh(
        o3d.utility.Vector3dVector(output_vertices),
        o3d.utility.Vector3iVector(output_triangles),
    )
    o3d.io.write_triangle_mesh(out_filename, out_mesh)

    print("Results:")
    print("Input  mesh: {} is manifold? {}".format(in_mesh, input_is_manifold))
    print("Output mesh: {} is manifold? {}".format(out_mesh, output_is_manifold))
    print(f'Ouput mesh has {len(output_vertices)} vertices and {len(output_triangles)} triangles, filename: {out_filename}')


def main():
    parser = argparse.ArgumentParser(description="Convert a triangular mesh to a watertight model.")
    parser.add_argument("input_path", help="Path to the input .obj file or directory containing .obj files")
    parser.add_argument("-d", "--depth", type=int, default=8, help="Depth for the conversion process (default: 8)")
    parser.add_argument("-o", "--output", default='/media/nio/data/car_mesh', help="Output directory for the converted meshes (default: '/media/nio/data/car_mesh')")
    args = parser.parse_args()

    input_path = args.input_path
    depth = args.depth
    output_dir = args.output

    if os.path.isdir(input_path):
        all_obj_files = glob(os.path.join(input_path, '*.obj'))
        for obj_file in all_obj_files:
            print(f'Processing {obj_file}')
            convert(obj_file, depth, output_dir)
    elif os.path.isfile(input_path):
        print(f'Processing {input_path}')
        convert(input_path, depth, output_dir)
    else:
        print(f"Invalid input path: {input_path}")


if __name__ == "__main__":
    main()
