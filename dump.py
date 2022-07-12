from src.util import read_json_list
from src.calculate import calculate_statistic


data = read_json_list('./data/schedule.jsonl')
statistic = calculate_statistic(data)

for day in sorted(statistic):
    print(day)
    stat = statistic[day]

    for p in stat['part']:
        print("",p,stat['part'][p],"h")
    print("","sum",stat['sum'],"h")








