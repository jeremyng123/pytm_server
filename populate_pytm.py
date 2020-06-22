from pytm.pytm import TM, Actor, Boundary, Dataflow, Datastore, Lambda, Server, Element, ExternalEntity, Process
import copy


class ThreatModel:
    def __init__(self, name, description="My TM", isOrdered=True, mergeResponses=True):
        self.tm = TM(name)
        self.tm.description=description
        self.tm.isOrdered = isOrdered
        self.tm.mergeResponses = mergeResponses

    def start(self):
        self.tm.process()


def replaceAttribute(obj, attr, val):
    setattr(obj, attr, val)


def makeBoundary(boundary_json):
    boundary_dict = copy.deepcopy(boundary_json)
    boundary = Boundary(boundary_dict.pop('name'))
    for k, v in boundary_dict.items():
        if k == 'description':
            boundary.description = v
        elif k == 'inBoundary':
            # should only do this when we have all the boundary objects in a dict. otherwise
            # this will have an error.
            continue
        elif k == 'Options':
            for option, v_ in v.items():
                replaceAttribute(boundary, option, v_)
    return boundary


def makeComponents(component_json, boundaryObj):
    component_dict = copy.deepcopy(component_json)
    component_cls = component_dict.pop('class')
    name = component_dict.pop('name')
    component = Element(name)
    if component_cls == 'Actor':
        component = Actor(name)
    elif component_cls == 'Server':
        component = Server(name)
    elif component_cls == 'Datastore':
        component = Datastore(name)
    elif component_cls == 'Lambda':
        component = Lambda(name)
    elif component_cls == 'ExternalEntity':
        component = ExternalEntity(name)
    elif component_cls == 'Process':
        component = Process(name)
    else:
        print(f"[WARNING] * Received weird class {component_cls} in makeComponents()")
        return None

    for k,v in component_dict.items():
        # print(v)
        if k == 'description':
            component.description = v
        elif k == 'inBoundary' and v is not '':
            component.inBoundary = boundaryObj[v]
        elif k == 'Options':
            for option, v_ in v.items():
                replaceAttribute(component, option, v_)
    return component


def makeDataflow(dataflow_json, componentObj, boundaryObj):
    name = dataflow_json.pop('name')
    if dataflow_json['source'] is not '' and dataflow_json['sink'] is not '':
        src = componentObj[dataflow_json.pop('source')]
        sink = componentObj[dataflow_json.pop('sink')]
    else:
        return None
    dataflow = Dataflow(src, sink, name)
    for k,v in dataflow_json.items():
        if k == 'Options':
            for option, v_ in v.items():
                replaceAttribute(dataflow, option, v_)
        else:
            if k == 'inBoundary':
                continue
            elif k == 'inBoundary' and v is not '':
                dataflow.inBoundary = boundaryObj[v]
                continue
            replaceAttribute(dataflow, k, v)

    return dataflow