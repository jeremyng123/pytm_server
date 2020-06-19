import json
from populate_pytm import *
import sys
import io


def decode(json):
    boundaryObj = {}
    componentObj = {}
    dataflowObj = {}
    tm = ThreatModel("test")
    for k,v in json.items():
        if k == "TM_Boundaries":
            for name, boundary in v.items():
                boundaryObj[name] = makeBoundary(boundary)

        elif k == "TM_Components":
            for class_, component in v.items():
                for uuid, json in component.items():
                    componentObj[uuid] = makeComponents(json, boundaryObj)

        elif k == "TM_Dataflows":
            for name_uuid, dataflow in v.items():
                dataflowObj[name_uuid] = makeDataflow(dataflow, componentObj)

        elif k == "TM_Diagrams":
            pass

    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    tm.start()

    newjson = new_stdout.getvalue()
    sys.stdout=old_stdout

    return newjson


if __name__ == '__main__':
    with open("exampleTM.json") as f:
        data = json.load(f)
        print(decode(data))