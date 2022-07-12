

def parseTime(time):
    h , m = time.split(':')
    return int(h) * 60 + int(m)

def get_duration(d):
    return parseTime(d['end']) - parseTime(d['start'])


def dataset_to_dict(data):
    data_dict = {}
    for d in data:
        k = d['date']
        if k not in data_dict: data_dict[k] = []
        data_dict[k].append(d)
    return data_dict
    

def split_dataset(data):
    base = []
    spents = []
    for d in data:
        duration = get_duration(d)
        if duration >= 4 * 60:
            base.append(d)
        else:
            spents.append(d)
            
    if len(base) != 1:
        raise ValueError(f"cannot parse {d}")
    #Todo validate spents duerfen sich nicht ueberschneiden und muessen in base liegen
    #base und spents muessen unterschiedliche projekte haben
    return base[0], spents


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
        base , spents = split_dataset(days[day])
        minutes = calculate(base,spents)
        stat = { "sum" : 0 , "part" : {}}
        for m in minutes:
            if m == "break": continue;
            if m.startswith("prj"):
                ah = adv_hours(minutes[m])
                stat['sum'] += ah
                stat['part'][m] = ah
        statistic[day] = stat
    return statistic