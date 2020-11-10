def read_from_offset(fp,start,limit,schema=None):
    data = []
    for i, line in enumerate(fp,start=start):
        if i < (start + limit):
            if schema:
                mdict = dict(zip(schema.replace('\n','').split(","),line.replace('\n','').split(",")))
                data.append(mdict)
            else:
                data.append(line)
    return data

def read_file_from_line(filepath,offset,limit):
    with open(filepath,"r",encoding="utf-8-sig") as fp:
        for i, line in enumerate(fp):
            if i == 0:
                schema = line
            if i == offset:
                print(f"starting from offset {offset}")
                data = read_from_offset(fp,offset,limit,schema=schema)
                return data