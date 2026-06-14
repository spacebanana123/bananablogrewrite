def template(text:str):
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
 
def tag(text:str):
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

def genericEntry(text:str):
    lines = text.split("\n")
    internal_dict = {}
    render_type = None
    keywords = ["extends", "tags", "date"]
    for line in lines:
        #Render type state mangement
        if line.strip().startswith("render"):
            render_type = line.strip().split(None, 1)[1]
            continue
        if line.strip().startswith("end render"):
            render_type = None
            continue
        if type(render_type) == str:
            render_dict = globals()[render_type](line)
            for key in render_dict:
                if key in internal_dict:
                    internal_dict[key].append(render_dict[key])
                else:
                    internal_dict[key] = [render_dict[key]]
        
        #Clearing out all other keywords to bypass processing.
        keyword_flag = False
        for keyword in keywords:
            if line.strip().startswith(keyword):
                keyword_flag = True
                break
        if keyword_flag:
            continue
    
    out_dict = {}
    for key in internal_dict:
        if len(internal_dict[key]) > 1:
            out_dict[key] = internal_dict[key][0]
        else: 
            out_str = ""
            for val in internal_dict[key]:
                out_str += f"{val}\n"
            out_dict[key] = out_str
    return internal_dict

class subrender:
    #this class renders individual lines with some amount of context information provided by the deligator.
    def general(line: str):