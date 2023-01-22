import datetime
import json
import os

from collections import defaultdict

START_EPOCH = 1673015280 * 1000000000

END_EPOCH = 1673015520 * 1000000000




def datetime_to_epoch(dt: datetime.datetime) -> int:
    pass


def epoch_to_datetime(ep: int) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(ep/1000000000)


def timestamp_to_datetime(ts: str) -> datetime.datetime:

    format = '%Y-%m-%d %H:%M:%S.%f'
    return datetime.datetime.strptime(ts[:-3], format)


def group_by_order_id(filename: str):
    data = load_json(filename)

    msgs_by_order_id = defaultdict(list)

    for i in range(len(data)):
        order_id = data[i]["OrderID"]
        msgs_by_order_id[order_id].append(data[i])


    with open(os.path.join("data", f"{filename[:-5]}ByOrderID.json"), "w") as outfile:
        json.dump(msgs_by_order_id, outfile)


def load_json(filename: str) -> json:
    with open(os.path.join("data", filename)) as fp:
        data = json.load(fp)
    return data



if __name__ == "__main__":

    pass


    #group_by_order_id("AequitasData.json")
    #group_by_order_id("AlphaData.json")
    #group_by_order_id("TSXData.json")

