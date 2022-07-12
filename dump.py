from src.util import read_json_list
from src.calculate import dataset_to_dict, split_dataset, calculate, adv_hours


data = read_json_list('./data/schedule.jsonl')
day = "2022-07-12"


days = dataset_to_dict(data)

for day in sorted(days):
    base , spents = split_dataset(days[day])

    minutes = calculate(base,spents)
    print(day)
    sumh = 0
    for m in minutes:
        if m == "break": continue;
        if m.startswith("prj"):
            ah = adv_hours(minutes[m])
            sumh += ah
            print("",m,ah,"h")
    print("","Summe",sumh,"h")








