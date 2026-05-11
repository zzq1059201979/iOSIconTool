import os
import platform

class FileService:
    @staticmethod
    def get_default_output_dir():
        if platform.system() == 'Darwin':
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        elif platform.system() == 'Windows':
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        else:
            desktop = os.path.expanduser('~')
        
        return os.path.join(desktop, 'iOSImages')

    @staticmethod
    def create_directory_if_not_exists(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
            return True
        return False

    @staticmethod
    def get_unique_filename(directory, filename):
        name, ext = os.path.splitext(filename)
        counter = 1
        new_filename = filename
        
        while os.path.exists(os.path.join(directory, new_filename)):
            new_filename = f"{name}_{counter}{ext}"
            counter += 1
        
        return new_filename

    @staticmethod
    def list_files_in_directory(directory, extensions=None):
        if not os.path.exists(directory):
            return []
        
        files = []
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isfile(full_path):
                if extensions is None or entry.lower().endswith(extensions):
                    files.append(full_path)
        
        return sorted(files)

    @staticmethod
    def get_file_size(file_path):
        if os.path.exists(file_path):
            return os.path.getsize(file_path)
        return 0

    @staticmethod
    def format_file_size(bytes_size):
        if bytes_size < 1024:
            return f"{bytes_size} B"
        elif bytes_size < 1024 * 1024:
            return f"{bytes_size / 1024:.2f} KB"
        else:
            return f"{bytes_size / (1024 * 1024):.2f} MB"
