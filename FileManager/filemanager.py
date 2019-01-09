import os


class FileManager:
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def get_file_path(self, file_name):
        return os.path.join(self.dir_path, file_name)

    @staticmethod
    def file_exists(file_path):
        if os.path.isfile(file_path):
            return True
        else:
            # File does not exist
            raise FileNotFoundError

    def read_file(self, file_name):
        file_path = self.get_file_path(file_name)
        if self.file_exists(file_path):
            with open(file_path, 'r') as f:
                # TODO: Perform tasks
                pass

    def write_file(self, file_name, data):
        file_path = self.get_file_path(file_name)
        with open(file_path, 'w') as f:
            # TODO: Perform tasks
            pass

    def delete_file(self, file_name):
        file_path = self.get_file_path(file_name)
        if self.file_exists(file_path):
            os.unlink(file_path)

