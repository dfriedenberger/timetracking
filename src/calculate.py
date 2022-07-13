

def parseTime(time):
    h , m = time.split(':')
    return int(h) * 60 + int(m)

def get_duration(d):
    return parseTime(d['end']) - parseTime(d['start'])

def get_projects(data):
    return set(map(lambda x: x['project'], data))


def dataset_to_dict(data):
    data_dict = {}
    for d in data:
        k = d['date']
        if k not in data_dict: data_dict[k] = []
        data_dict[k].append(d)
    return data_dict
    

def validate_union(spent1,spent2):
    s1 = parseTime(spent1['start']) 
    e1 = parseTime(spent1['end']) 
    s2 = parseTime(spent2['start'])
    e2 = parseTime(spent2['end'])

    if e1 <= s1: raise ValueError(f"end before start {spent1}")
    if e2 <= s2: raise ValueError(f"end before start {spent2}")

    if e1 <= s2: return #spent1 before spent2
    if e2 <= s1: return #spent2 before spent1

    raise ValueError(f"union exists between {spent1} and {spent2}")

def is_inside(base,spent):
    sb = parseTime(base['start']) 
    eb = parseTime(base['end']) 
    s = parseTime(spent['start'])
    e = parseTime(spent['end'])

    if sb <= s and e <= eb:
        return True
    if e <= sb: return False #spent before base
    if sb <= e: return False #base before spent

    raise ValueError(f"union exists between {base} and {spent}")


def split_dataset(data):
    base = []
    spents = []
    for d in data:
        duration = get_duration(d)
        if duration >= 4 * 60:
            base.append(d)
        else:
            spents.append(d)


    #Validation  
    if len(base) > 1:
        raise ValueError(f"cannot parse {d}")

    #Validate spents duerfen sich nicht ueberschneiden 
    l = len(spents)
    for x in range(l):
        for y in range(x+1,l):
            #Validate
            validate_union(spents[x],spents[y])

    #Validate base und spents muessen unterschiedliche projekte haben
    projects_base = get_projects(base)
    projects_spents = get_projects(spents)
    project_intersections = projects_base.intersection(projects_spents)
    if len(project_intersections) > 0:
        raise ValueError(f"base and spent have same projects {project_intersections}")

    if len(base) == 1:        
        return base[0], spents
    if len(base) == 0:
        return { "project" : "default" , "start" : "06:00" , "end" : "22:00"}, spents

    raise ValueError(f"not implemented")

def calculate(base,spents):
    
    minutes = {}
    base_project = base['project']
    minutes[base_project] = get_duration(base)
    for spent in spents:
        spent_minutes = get_duration(spent)
        spent_project = spent['project']
        if spent_project not in minutes:
            minutes[spent_project] = 0
        minutes[spent_project] += spent_minutes
        #if inside base
        if is_inside(base,spent):
            minutes[base_project] -= spent_minutes
    return minutes

def adv_hours(minutes):
    h = minutes % 60
    rest = minutes - h * 60
    v = round(rest / 15)
    return h + v * 0.25

def calculate_statistic(data):
    days = dataset_to_dict(data)
    statistic = {}
    for day in sorted(days):
        try: 
            base , spents = split_dataset(days[day])
            minutes = calculate(base,spents)
            stat = { "status" : "Ok" , "sum" : 0 , "part" : {}}
            for m in minutes:
                if m == "break": continue;
                if m == "default": continue;
                if m.startswith("prj"):
                    ah = adv_hours(minutes[m])
                    stat['sum'] += ah
                    if m not in stat['part']: stat['part'][m] = 0
                    stat['part'][m] += ah
            statistic[day] = stat
        except ValueError as e:
            statistic[day] = { "status" : "Failed" , "message" : str(e)}
    return statistic