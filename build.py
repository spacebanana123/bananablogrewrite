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
    #Check that we have static files at all. 
    if not (os.path.exists(STATIC_DIR)):
        return
    
    #If we do, the flow ends up here, and we copy everthing.
    shutil.copytree(STATIC_DIR, PUBLIC_DIR)

class entry:
    #TODO: Custom CSS support. 
    def constructor(text:str,renderer:function = lambda x: x,extends:str = "default",tags:list = []) -> entry:
        new_entry = entry()
        new_entry.extends = extends
        new_entry.tags = tags
        new_entry.renderer = renderer
        new_entry.text = text
        return new_entry
    
	#Print statement for debugging
    def print(self):
        print(f"Extends:{self.extends}\nTags:{self.tags}\nRender:{self.renderer}\nText:{self.text}\n")

    #Semantic sugar for rendering out an entry.
    def render(self) -> dict:
        return self.renderer(self.text)
    
    #Take rendered content and insert it into a template.
    def extend(self) -> str:
        #Check that template does actually exist.
        if not os.path.isfile(self.extends):
            return None
        #Open file and replace.
        with open(self.extends, "r") as template:
            final_content = template.read()
            entry_rendered = self.render()
            for key in entry_rendered:
                final_content.replace(f"<!--{key}-->",entry_rendered[key])
            return final_content
        return None

def main():
    print("Build starting...")

    initFolders()

    copyStaticFiles()

    with open(TEMPLATES_DIR, "") as template_folder:
        if not os.path.isdir(template_folder):

        for template in template_folder:
            with open(template, "r") as template_text: 
                template_entry = entry.constructor(template_text)

if __name__ == '__main__':
    main()