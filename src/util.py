import json

def read_json_list(filename):
    json_list = []
    with open(filename, 'r',encoding='utf-8') as f:
        time_spents = list(f)

        for time_spent in time_spents:
            result = json.loads(time_spent)
            json_list.append(result)
    return json_list


def write_json_list(filename,json_list):
    with open(filename, 'w', encoding='utf-8') as f:
        for d in json_list:
            f.write(json.dumps(d,ensure_ascii=False) +"\n")


def delete_by_id(data,id):
    for i in range(len(data)):
        if id == data[i]['id']:
            del data[i]