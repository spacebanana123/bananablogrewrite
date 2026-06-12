import os
import shutil
import operator

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR,"static")
ENTRIES_DIR = os.path.join(ROOT_DIR, "entries")
TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")
TEMP_DIR = os.path.join(ROOT_DIR, "temp")
TEMP_TEMPLATES_DIR = os.path.join(TEMP_DIR,".templates")
PUBLIC_DIR = os.path.join(ROOT_DIR,"public")
DEFAULT_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR,"default.html")

# Clears out possible old files and then initialized new folders for us to use. 
def initFolders():
    dirs_to_clean = [PUBLIC_DIR,TEMP_DIR,TEMP_TEMPLATES_DIR]

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
    def constructor(text:str,renderer:function = lambda x: x,extends:str = "default.html",tags:list = [],priority = 0,date = "yyyy-mm-dd hr:mm") -> entry:
        new_entry = entry()
        new_entry.extends = extends
        new_entry.tags = tags
        new_entry.renderer = renderer
        new_entry.text = text
        new_entry.priority = priority
        new_entry.date = date
        return new_entry
    
	#Print statement for debugging
    def print(self):
        print(f"Extends:{self.extends}\nTags:{self.tags}\nRender:{self.renderer}\nText:{self.text}\n")

    #Key for sorting
    def key(self):
        return (self.priority,self.date)

    def extractExtends(text:str):
        extends = "default.html"
        lines = text.split("\n")
        for line in lines: 
            if line.strip().startswith("extends"):
                extends = line.strip().split(None, 1)[1]
        if not extends.endswith(".html"):
            extends += ".html"
        return extends

    def extractTags(text:str):
        tags = []
        lines = text.split("\n")
        for line in lines: 
            if line.strip().startswith("tags"):
                split_line = line.strip().split()
                tags = split_line[1:len(split_line)]
        return tags
    
    def extractDate(text:str):
        date_entry = ""
        lines = text.split("\n")
        for line in lines: 
            if line.strip().startswith("date"):
                date_entry = line.strip().split(None, 1)[1]
        return date_entry

    #Semantic sugar for rendering out an entry.
    def render(self) -> dict:
        return self.renderer(self.text)
    
    #Take rendered content and insert it into a template.
    #If render_level = -1, use the pre-rendering templates, instead of post rendering templates. 
    def extend(self, render_level = 1) -> str:
        #Setdir of template
        template_path = os.path.join(TEMP_TEMPLATES_DIR,self.extends)
        if render_level == -1:
            template_path = os.path.join(TEMPLATES_DIR,self.extends)
        #Check that template does actually exist.
        if not os.path.isfile(template_path):
            return None
        #Open file and replace based on keys from rendered content.
        with open(template_path, "r") as template:
            final_content = template.read()
            entry_rendered = self.render()
            for key in entry_rendered:
                final_content = final_content.replace(f"<!--{key}-->",entry_rendered[key])
            return final_content


#Deal with all of the templates by treating them as entries. 
def process_templates():
    #Open all the templates. 
    templates = os.listdir(TEMPLATES_DIR)
    next_templates = []
    #Counter exists solely to have a HARD CAP on recursive behavior
    # that could otherwise result from this method of processing
    counter = 0
    while counter == 0 or (counter < 100 and len(next_templates) > 0): 
        for template_path in templates:
            #Check if this is a default template. If so, we don't need to do any processing to it. 
            if template_path.endswith("default.html"):
                shutil.copy(os.path.join(TEMPLATES_DIR,template_path),os.path.join(TEMP_TEMPLATES_DIR,template_path))
            #If it isn't a default template, read it, pack it as a template entry and then have it extend whatever it is supposed to. 
            else:
                with open(os.path.join(TEMPLATES_DIR,template_path),"r") as template:
                    text = template.read()
                    template_entry = entry.constructor(text,
                                                    render_template,
                                                    entry.extractExtends(text))
                    with open(os.path.join(TEMP_TEMPLATES_DIR,template_path), "w") as out_template:
                        text_to_write = template_entry.extend()
                        if text_to_write == None:
                            #None means there is a missing template file
                            #That could be because the template file we are searching for is later in the queue
                            #or dependent on some template later in the queue. 
                            #thus by adding the template to the next list, 
                            #we can process templates that are dependent on multiple layers of templates.
                            #This DOES carry a performance penalty, which is a possibility for improvement. 
                            next_templates.append(template_path)
                        else: 
                            out_template.write(text_to_write)
        counter += 1
        templates = next_templates

def process_entries():
    entries = os.listdir(ENTRIES_DIR)
    tag_tracker = {}
    for file in entries:
        #Steps to the process:
        #1. Find what template we should use. 
        #2. Find what render function we shoud use
        #3. Find and track tags. 
        #4. Spit out processed html page for dedicated page for the entry. 
        #5. Spit out tag pages
        #6. Spit out index page that contains links to every tag and entry.
        with open(os.path.join(ENTRIES_DIR,file)) as entry_file:
            entry_text = entry_file.read()
            template = entry.extractExtends(entry_text)

            #TODO: Finding render function needs implementation. Maybe another keyword would work. 
            #For now we will use a general function
            renderer = render_generic_entry

            tags = entry.extractTags(entry_text)

            entry_date = entry.extractTags(entry_text)

            new_entry = entry.constructor(entry_text, renderer, template, tags,entry_date)
            new_filename = file.split(".")[0] + ".html"

            #tracking globally across all files all tags and files associated with those tags.
            for tag in tags:
                try:
                    tag_tracker[tag].append(new_entry)
                except:
                    tag_tracker[tag] = [new_entry]

            with open(os.path.join(TEMP_DIR,new_filename),"w") as out_file:
                text_to_write = new_entry.extend()
                if text_to_write == None:
                    continue
                else: 
                    out_file.write(text_to_write)
    
    #Writing tag pages. 
    for tag in tag_tracker:
        if os.path.exists(os.path.join(TEMP_TEMPLATES_DIR,f"{tag}.html")):
            tag_template = f"{tag}.html" #We have a tag specific template
        else: 
            tag_template = "tag.html" #Use the default tag template
        tag_tracker[tag] = sorted(tag_tracker[tag], key=operator.methodcaller("key"))
        for tagged_entry in tag_tracker[tag]:
            text_to_write = tagged_entry.render()["body"]
            if text_to_write == None:
                continue
            else: 
                entry_text += f"<div>{text_to_write}</div>\n"

        tag_entry = entry.constructor(entry_text,render_tag,tag_template)
        with open(os.path.join(TEMP_DIR,f"{tag}.html"),"w") as out_file:
            text_to_write = tag_entry.extend()
            if text_to_write == None:
                continue
            else: 
                out_file.write(text_to_write)

def export_temp_folder():
    
    for file in os.listdir(TEMP_DIR):
        #ignore all files that start with .
        #we can change this in the future to be more modifiable.
        if not file.startswith("."):
            if os.path.isdir(os.path.join(TEMP_DIR,file)):
                shutil.copytree(os.path.join(TEMP_DIR,file), os.path.join(PUBLIC_DIR,file))
            else: 
                shutil.copy(os.path.join(TEMP_DIR,file), os.path.join(PUBLIC_DIR,file))

# --- RENDER FUNCTIONS ---
#Consider making this a different file? It would be more organized overall
def render_template(text:str):
    lines = text.split("\n")
    out_lines = []
    for line in lines: 
        if line.strip().startswith("\\"):
            out_lines.append(line.strip()[1:len(line)])
        elif line.strip().startswith("extends"):
            pass
        else:
            out_lines.append(line)
    out_str = ""
    for out_line in out_lines:
        out_str += out_line + "\n"
    return {"body":out_str}          
 
def render_tag(text:str):
    lines = text.split("\n")
    out_lines = []
    tag = ""
    description = "None entered"
    for line in lines: 
        if line.strip().startswith("\\"):
            out_lines.append(line.strip()[1:len(line)])
        elif line.strip().startswith("tag"):
            tag = line.strip().split(None, 1)[1]
        elif line.strip().startswith("description"):
            description = line.strip().split(None, 1)[1]
        else:
            out_lines.append(line)
    out_str = ""
    for out_line in out_lines:
        out_str += out_line + "\n"
    return {"body":out_str,
            "title": tag,
            "tag": tag,
            "description": description}          

def render_generic_entry(text:str):
    lines = text.split("\n")
    body_lines = []
    title = ""
    for line in lines:
        if line.strip().startswith("\\"):
            body_lines.append(line.strip()[1:len(line)])
        elif line.strip().startswith("#"):            
            title = line.strip()[1:len(line)].strip()
            body_lines.append(title)
        elif line.strip().startswith("extends"):
            pass
        elif line.strip().startswith("tags"):
            pass
        elif line.strip().startswith("date"):
            pass
        else:
            body_lines.append(line)

    body_str = ""
    for body_line in body_lines:
        body_str += f"{body_line}\n"
    return {"body": body_str,
            "title": title}

def main():
    print("Build starting...")

    initFolders()
    print("Folders initialized")

    copyStaticFiles()
    print("Static files copied")

    process_templates()
    print("Templates rendered")

    process_entries()
    print("Entries processed")

    export_temp_folder()
    print("Temp folder exported")

    
if __name__ == '__main__':
    main()