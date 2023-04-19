import trimesh
import zipfile
from glob import glob
from pathlib import Path
import shutil
import os
from loguru import logger
import subprocess
import concurrent.futures
import argparse

parser = argparse.ArgumentParser(description="Mesh preprocessing script")
parser.add_argument("--base_dir", type=str, required=True, help="Base directory containing .obj files")
parser.add_argument("--output_dir", type=str, required=True, help="Output directory for processed meshes")
parser.add_argument("--processed_dir", type=str, required=True, help="Directory for processed mesh files")
parser.add_argument("--executable", type=str, required=True, help="Path to PreprocessMesh executable")
parser.add_argument("--num_threads", type=int, default=14, help="Number of threads to use (default: 14)")
args = parser.parse_args()

os.makedirs(args.output_dir, exist_ok=True)
os.makedirs(args.processed_dir, exist_ok=True)

def process_mesh(mesh_filepath, target_filepath):
    logger.info(mesh_filepath + " --> " + target_filepath)
    if os.path.exists(target_filepath):
        return
    command = [args.executable, "-m", mesh_filepath, "-o", target_filepath]

    subproc = subprocess.Popen(command, stdout=subprocess.DEVNULL)
    subproc.wait()

meshes_targets_and_specific_args = []

all_obj_files = glob(args.base_dir + '/*.obj')

for obj_file in all_obj_files:
    try:
        mesh_name = Path(obj_file).stem

        target_filepath = f'{args.processed_dir}/{mesh_name}.npz'
        logger.info(all_obj_files[0] + " --> " + target_filepath)
        
        meshes_targets_and_specific_args.append(
            (
                obj_file,
                target_filepath
            )
        )
    except Exception as e:
        logger.error(e)
        
with concurrent.futures.ThreadPoolExecutor(
        max_workers=int(args.num_threads)
    ) as executor:

        for (
            mesh_filepath,
            target_filepath,
        ) in meshes_targets_and_specific_args:
            executor.submit(
                process_mesh,
                mesh_filepath,
                target_filepath
            )

        executor.shutdown()
