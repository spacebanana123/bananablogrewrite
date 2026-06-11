import os
import shutil

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR,"static")
ENTRIES_DIR = os.path.join(ROOT_DIR, "entries")
TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")
TEMP_DIR = os.path.join(ROOT_DIR, "temp")
PUBLIC_DIR = os.path.join(ROOT_DIR,"public")
DEFAULT_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR,"default.html")

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
    for file in os.listdir(STATIC_DIR):
        shutil.copy(os.path.join(STATIC_DIR,file),os.path.join(TEMP_DIR,file))

#We treat both entries and templates as entries. Both extend other things and can be rendered out. 
class entry:
    #TODO: Custom CSS support. 
    def constructor(text:str,renderer:function = lambda x: x,extends:str = "default.html",tags:list = []) -> entry:
        new_entry = entry()
        new_entry.extends = extends
        new_entry.tags = tags
        new_entry.renderer = renderer
        new_entry.text = text
        return new_entry
    
	#Print statement for debugging
    def print(self):
        print(f"Extends:{self.extends}\nTags:{self.tags}\nRender:{self.renderer}\nText:{self.text}\n")

    def extractExtends(text:str):
        extends = "default.html"
        lines = text.split("\n")
        for line in lines: 
            if line.strip().startswith("extends"):
                extends = line.strip().split(1)[1]
        return extends

    #Semantic sugar for rendering out an entry.
    def render(self) -> dict:
        return self.renderer(self.text)
    
    #Take rendered content and insert it into a template.
    def extend(self) -> str:
        #Check that template does actually exist.
        if not os.path.isfile(os.path.join(TEMPLATES_DIR,self.extends)):
            return None
        #Open file and replace.
        with open(os.path.join(TEMPLATES_DIR,self.extends), "r") as template:
            final_content = template.read()
            entry_rendered = self.render()
            for key in entry_rendered:
                final_content.replace(f"<!--{key}-->",entry_rendered[key])
            return final_content
        return None

def render_template(text:str):
    lines = text.split("\n")
    out_lines = []
    for line in lines: 
        if line.strip().startswith("\\"):
            out_lines.append(line.strip()[1:len(line)])
        elif line.strip().startswith("extends"):
            continue
        else:
            out_lines.append(line)
    return out_lines
            

#Deal with all of the templates by treating them as entries. 
def process_templates():
    #Open all the templates. 
    templates = os.listdir(TEMPLATES_DIR)
    for template_path in templates:
        if template_path.endswith("default.html"):
            shutil.copy(os.path.join(TEMPLATES_DIR,template_path),os.path.join(TEMP_DIR,template_path))
        else:
            with open(os.path.join(TEMPLATES_DIR,template_path),"r") as template:
                text = template.read()
                template_entry = entry.constructor(text,
                                                   render_template,
                                                   entry.extractExtends(text))
                with open(os.path.join(TEMP_DIR,template_path), "w") as out_template:
                    out_template.write(template_entry.extend())

def main():
    print("Build starting...")

    initFolders()

    copyStaticFiles()

    process_templates()

    
if __name__ == '__main__':
    main()