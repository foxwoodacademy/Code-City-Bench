from huggingface_hub import HfApi

api = HfApi()

# Create the dataset repo first if it doesn't exist
repo_id = "foxwoodadmin/mrs-higgins-pipeline"

# Upload the folder
api.upload_folder(
    repo_id=repo_id,
    folder_path="/storage/emulated/0/RootBase/mrs_higgins_saas",
    repo_type="dataset"
)

print("Upload complete!")
