import os

ALLOWED_EXTENSIONS = [".py", ".md", ".txt", ".cpp"]


def filter_files(file):

    for ext in ALLOWED_EXTENSIONS:
        if file.endswith(ext):
            return True

    return False


def get_all_files(repo_path):

    all_files = []

    for root, dirs, files in os.walk(repo_path):

        for file in files:

            if filter_files(file):

                full_path = os.path.join(root, file)

                all_files.append(full_path)

    return all_files
