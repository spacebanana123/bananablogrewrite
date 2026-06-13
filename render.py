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
    body_lines = []
    out_dict = {}
    title = ""
    line_num = 0
    keywords = ["extends", "tags", "date"]
    for i, line in enumerate(lines):
        if not i <= line_num:
            continue
        if line.strip().startswith("render"):
            func_to_call = line.strip().split(None, 1)[1]
            if func_to_call in dir():
                render_out = globals()[func_to_call](text , i)
                dict = render_out[0]
                line_num = render_out[1]
                for key in dict:
                    if key == "body":
                        body_line += dict["body"]
                    else:
                        out_dict[key] = dict[key]
            continue
        #non-render keywords management
        keyword_flag = False
        for keyword in keywords:
            if line.strip().startswith(keyword):
                keyword_flag = True
                break
        if keyword_flag:
            continue
        if line.strip().startswith("\\"):
            body_lines.append(line.strip()[1:len(line)])
        elif line.strip().startswith("#"):            
            title = line.strip()[1:len(line)].strip()
            body_lines.append(title)
        else:
            body_lines.append(line)

    body_str = ""
    for body_line in body_lines:
        body_str += f"{body_line}\n"
    out_dict["body"] = body_str
    out_dict["title"] = title
    return out_dict