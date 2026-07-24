import zipfile
import os

def create_zip(source_dir, output_filename):
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Ensure we store paths relative to the project root
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)

if __name__ == "__main__":
    os.makedirs("/storage/emulated/0/GRAB/", exist_ok=True)
    create_zip("CodeCity-Bench", "/storage/emulated/0/GRAB/CodeCity-Bench-v0.1.zip")
    print("Zip created at /storage/emulated/0/GRAB/CodeCity-Bench-v0.1.zip")
