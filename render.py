keywords = ["extends", "tags", "date", "description", "priority"]

def template(text:str):
    lines = text.split("\n")
    out_lines = []
    internal_dict = {}
    for line in lines: 
        #Clearing out all other keywords to bypass processing.
        keyword_flag = False
        for keyword in keywords:
            if line.strip().startswith(keyword):
                keyword_flag = True
                break
        if keyword_flag:
            if line.strip().startswith("description"):
                internal_dict["description"] = line.strip().split(None, 1)[1]
            continue
        
        if line.strip().startswith("\\"):
            out_lines.append(line.strip()[1:len(line)])
        else:
            out_lines.append(line)
    out_str = ""
    for out_line in out_lines:
        out_str += out_line + "\n"
    internal_dict["body"] = out_str
    return internal_dict        
 
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
    render_type = "general"
    for line in lines:
        #Render type state mangement
        if line.strip().startswith("render"):
            render_type = line.strip().split(None, 1)[1]
            continue
        if line.strip().startswith("end render"):
            render_type = "general"
            continue
        
        if render_type == "general":
            #Clearing out all other keywords to bypass processing.
            keyword_flag = False
            for keyword in keywords:
                if line.strip().startswith(keyword):
                    keyword_flag = True
                    break
            if keyword_flag:
                continue

        render_func = getattr(subrender,render_type)
        render_dict = render_func(line)
        for key in render_dict:
            if key in internal_dict:
                internal_dict[key].append(render_dict[key])
            else:
                internal_dict[key] = [render_dict[key]]
        
    
    out_dict = {}
    for key in internal_dict:
        if len(internal_dict[key]) == 1:
            out_dict[key] = internal_dict[key][0]
        else: 
            out_str = ""
            for val in internal_dict[key]:
                out_str += f"{val}\n"
            out_dict[key] = out_str

    return out_dict

class subrender:
    #this class renders individual lines with some amount of context information provided by the deligator.
    def general(line: str):
        out_dict = {}
        out_end_dict = {}
        processed_line = line.strip()

        header_num = 0
        if processed_line.startswith("#"):
            for (i,char) in enumerate(processed_line):
                if(char == "#"):
                    continue
                else: 
                    header_num = i + 1
                    break
            if header_num == 2:
                out_dict["title"] = processed_line.split(None,1)[1]

            if "body" in out_dict:
                out_dict["body"] += f"<h{header_num} id=\"{processed_line.split(None,1)[1].replace(" ","_")}\">"
                out_dict["body"] += f"<a href=\"#{processed_line.split(None,1)[1].replace(" ","_")}\">"
            else: 
                out_dict["body"] = f"<h{header_num} id=\"{processed_line.split(None,1)[1].replace(" ","_")}\">"
                out_dict["body"] += f"<a href=\"#{processed_line.split(None,1)[1].replace(" ","_")}\">"   
            if "body" in out_end_dict:
                out_end_dict["body"] +=  "</a>"
                out_end_dict["body"] += f"</h{header_num}>"
            else: 
                out_end_dict["body"] =  "</a>"
                out_end_dict["body"] += f"</h{header_num}>"
            out_dict["body"] += processed_line.split(None,1)[1]

        elif processed_line.startswith("\\"):
            processed_line = processed_line[1:len(line)]

        # Every line is a paragraph of its own, so if the line is not empty 
        # (with maybe more restrictions in the future)
        # we add p tags to both sides of the line
        elif len(processed_line) > 0:
            if "body" in out_dict:
                out_dict["body"] += "<p>"
            else: 
                out_dict["body"] = "<p>"

            if "body" in out_end_dict:
                out_end_dict["body"] += "</p>"
            else: 
                out_end_dict["body"] = "</p>"

            out_dict["body"] += processed_line

        for key in out_end_dict:
            if key in out_dict:
                out_dict[key] += out_end_dict[key]
            else:
                out_dict[key] = out_end_dict[key]

        return out_dict
    
    def index(line: str):
        return subrender.general(line)
    def music(line: str):
        if line.startswith("review_score"):
            return {"body": f"<p>⭐{line.split(None,1)[1]}/10.0</p>"}
        return subrender.general(line)