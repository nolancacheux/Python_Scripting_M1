import os

def list_files_in_folder(folder_path):
    try:
        files = os.listdir(folder_path)
        for file in files:
            print(file)
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
folder_path = 'E:\\ISEN\\Enseignement\\2024-2025\\Python'
list_files_in_folder(folder_path)