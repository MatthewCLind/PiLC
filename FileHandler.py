from Components import *
from Events import *
import json


def _load_object_from_json(filename, node=''):
    """
    Private function
    Performs a loads() on the data from filename
    :param filename: relative path to file
    :type filename: str
    :param node: optionally cleaves a part of the dict and only returns data from node
    """
    with open(filename, 'r') as f:
        def_str = f.read()

    temp_dict = None
    if def_str != '':
        load_dict = json.loads(def_str)
        if node != '':
            temp_dict = load_dict[node]

    return temp_dict


def _save_dict(filename, data):
    """
    Private function
    Saves to a file
    :param filename: File path (will overwrite all data in file)
    :type filename: str
    :param data: object to save as json
    """
    definition_json_str = json.dumps(data, indent=4)
    with open(filename, 'w') as f:
        f.write(definition_json_str)


def _create_events_definition(current_events):
    """
    Private function
    Puts together a list of save-able event definitions
    :type current_events: list[Event]
    :rtype: list
    """
    event_definitions = []

    for event in current_events:
        ev_def = event.get_definition()
        event_definitions.append(ev_def)

    return event_definitions


def _create_components_definition(current_comps):
    """
    Private function
    Puts together a list of save-able component definitions
    :type current_comps: list[Component]
    :rtype: dict
    """
    comp_definitions = {}

    for comp in current_comps:
        comp_type, comp_def = comp.get_definition()
        if comp_type not in comp_definitions:
            comp_definitions[comp_type] = []
        comp_definitions[comp_type].append(comp_def)

    return comp_definitions


def load_events_definition(all_components):
    """
    Creates the events list from the definitions.json save file
    :type all_components: list[Component]
    :return: either a list of events, or None if there was nothing in the file
    """
    evs_dict = _load_object_from_json('definitions.json', 'EVENTS')
    events = None
    if evs_dict is not None:
        events = create_events(all_components, events_list=evs_dict)
    return events


def load_components_definition():
    """
    Creates components from the definitions.json save file
    :return: either a list of Componetns or None if there's nothing in the file
    """
    comp_dict = _load_object_from_json('definitions.json', 'COMPONENTS')
    components = None
    if comp_dict is not None:
        components = create_components(components_dict=comp_dict)
    return components


def load_client_updates(all_components):
    """
    Grabs updates from the web-app, such as new Components
    In the future there may also be commands and such
    :type all_components: [Component]
    :return: [Component], [Event] or None if there's nothing new
    """
    updates_dict = _load_object_from_json('client_updates.json')

    new_events = None
    new_comps = None

    if 'COMPONENTS' in updates_dict:
        comps_dict = updates_dict['COMPONENTS']
        new_comps = create_components(components_dict=comps_dict)

    if 'EVENTS' in updates_dict:
        evs_dict = updates_dict['EVENTS']
        new_events = create_events(all_components, events_list=evs_dict)

    return new_comps, new_events


def save_definition(current_comps=None, current_events=None):
    """
    Save the master file, definitions.json
    ** This function overwrites everything in definitions.json
    ** Make sure you give all necessary information, lest your progress be lost forever
    :type current_comps: list[Component]
    :type current_events: list[Event]
    """
    comp_definitions = _create_components_definition(current_comps)
    event_definitions = _create_events_definition(current_events)
    definition_dict = {'EVENTS': event_definitions, 'COMPONENTS': comp_definitions}
    _save_dict('definitions.json', definition_dict)


def send_client_components(current_comps):
    """
    Saves components to current_components.json for use by web-app
    :type current_comps: list[Component]
    """
    comp_definitions = _create_components_definition(current_comps)
    _save_dict('current_components.json', comp_definitions)


def send_client_events(current_events):
    """
    Saves events to current_events.json for use by web-app
    :type current_events: list[Event]
    :return:
    """
    event_definitions = _create_events_definition(current_events)
    _save_dict('current_events.json', event_definitions)


def save_live_feed(all_components):
    """
    Saves components' display data to live_feed.json for web-app
    :type all_components: list[Component]
    """
    live_feed_dict = {}
    for component in all_components:
        c_type, display_dict = component.get_display()
        if c_type not in live_feed_dict:
            live_feed_dict[c_type] = []
        live_feed_dict[c_type].append(display_dict)
    _save_dict('live_feed.json', live_feed_dict)
