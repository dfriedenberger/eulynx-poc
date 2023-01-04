import os
import logging

# Helper
def to_path(o):
    return o.lower().replace(' ','-')

class Project:

    def __init__(self,name,path):
        self.name = name
        self.path = path

    def create_project(self,name):
        return Project(name,f"{self.path}/{to_path(name)}")

    def init(self):
        logging.info(f"Implement Project {self.name} in path {self.path}")
        if not os.path.exists(self.path):
            logging.info(f'Create path {self.path}')
            os.mkdir(self.path)

    def create_file(self,filename,content):
        dst_file = os.path.join(self.path,filename)
        with open(dst_file, 'w') as f:
            f.write(content)
            
    def create_folder(self,foldername):
        dst_folder = os.path.join(self.path,foldername)
        if not os.path.exists(dst_folder):
            logging.info(f'Create path {dst_folder}')
            os.mkdir(dst_folder)