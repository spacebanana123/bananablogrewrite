import os
import shutil

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR,"static")
ENTRIES_DIR = os.path.join(ROOT_DIR, "entries")
TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")
TEMP_DIR = os.path.join(ROOT_DIR, "temp")
PUBLIC_DIR = os.path.join(ROOT_DIR,"public")

# Clears out possible old files and then initialized new folders for us to use. 
def initFolders():
    dirs_to_clean = [PUBLIC_DIR,TEMP_DIR]

    for dir in dirs_to_clean:
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)
    

# We know that static files don't need to modified in any way and can be directly copied over to the public folder. 
def copyStaticFiles():
    if not (os.path.exists(STATIC_DIR)):
        return
    
    shutil.copytree(STATIC_DIR, PUBLIC_DIR)

class template:
    def constructor(self,renderer:function,text:str,extends:str = "default",tags:list = []):
        self.extends = extends
        self.tags = tags
        self.renderer = renderer
        self.text = text
    
    def render(self):
        return self.renderer(self.text)
    
    def extend(self):
        with open()
    




def main():

    print("Build starting...")

    initFolders()


if __name__ == '__main__':
    main()