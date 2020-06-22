import json
from populate_pytm import *
import sys
import io


def decode(json):
    boundaryObj = {}
    componentObj = {}
    dataflowObj = {}
    tm = ThreatModel("test",isOrdered=False)
    for k,v in json.items():
        # print(v)
        if k == "TM_Boundaries":
            for name, boundary in v.items():
                boundaryObj[name] = makeBoundary(boundary)

        elif k == "TM_Components":
            for class_, component in v.items():
                for uuid, json in component.items():
                    componentObj[uuid] = makeComponents(json, boundaryObj)

        elif k == "TM_Dataflows":
            for name_uuid, dataflow in v.items():
                dataflowObj[name_uuid] = makeDataflow(dataflow, componentObj, boundaryObj)

        elif k == "TM_Diagrams":
            pass
    # print(componentObj)
    # print(dataflowObj)

    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    tm.start()

    newjson = new_stdout.getvalue()
    sys.stdout=old_stdout

    return newjson


if __name__ == '__main__':
    # with open("exampleTM.json") as f:
    with open("data.json") as f:
        data = json.load(f)
        print(decode(data))