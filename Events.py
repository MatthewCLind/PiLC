import json


class Event(object):
    """
    Events are what make things happen. Each event has a Condition and an Effect.
    Conditions keep track of what should be true in order for the Effect to happen.
    Effects call the proper methods to induce action

    Optionally, an Event can be deactivated or re-activated based on self.activate_condition and
        self.deactivate_condition
    """

    def __init__(self, label, condition, effect, activate_condition=None, deactivate_condition=None):
        """
        :param label: User-defined name of this event
        :type condition: Condition
        :type effect: Effect
        :param activate_condition: Condition which controls when this Event should be re-activated
        :type activate_condition: Condition
        :param deactivate_condition: Condition which controls when this event should be deactivated
                (meaning no longer evaluates)
        :type deactivate_condition: Condition
        """
        self.label = label
        self.activate_condition = activate_condition
        self.deactivate_condition = deactivate_condition
        self.condition = condition
        self.effect = effect
        self.state = 'ACTIVE'

    def __str__(self):
        return self.label + ':\n\tconditions: ' + str(self.condition) + '\n\teffects: ' + str(self.effect)

    def get_label(self):
        return self.label

    def set_state(self, state):
        """
        state should be either 'ACTIVE' or 'DEACTIVATED'
        :param state:
        :type state: str
        """
        self.state = state  # type: str

    def evaluate(self):
        """
        Basically causes the event to chooch
        """

        # If it isn't active, don't do anything
        if self.state == 'ACTIVE' and self.condition.evaluate():
            self.effect.perform_actions()

        # determine state
        if self.deactivate_condition is not None:
            if self.state == 'ACTIVE' and self.deactivate_condition.evaluate():
                self.set_state('DEACTIVATED')
        if self.activate_condition is not None:
            if self.state == 'DEACTIVATED' and self.activate_condition.evaluate():
                self.set_state('ACTIVE')

    def get_definition(self):
        """
        Creates an entry for saving this event to disk
        :return: the entry
        :rtype: dict
        """
        cond_def = self.condition.get_definition()
        eff_def = self.effect.get_definition()

        identity = {'LABEL': self.label, 'CONDITIONS': cond_def, 'EFFECTS': eff_def}

        if self.activate_condition is not None:
            activate_def = self.activate_condition.get_definition()
            identity['ACTIVATE'] = activate_def

        if self.deactivate_condition is not None:
            deactivate_def = self.deactivate_condition.get_definition()
            identity['DEACTIVATE'] = deactivate_def

        return identity


class Condition(object):
    """
    Keeps track of all of the necessary states of relevant components for its Event
    """

    def __init__(self, checks):
        """
        :type checks: list
        """
        self.checks = checks

    def __str__(self):
        return str(self.checks)

    def evaluate(self):
        """
        Function which determines if the all of the conditions are met
        :rtype: bool
        """
        all_conditions_met = True

        for entry in self.checks:
            component = entry['COMPONENT']
            method_name = entry['METHOD']
            val = entry['VALUE']
            current_condition = component.evaluate_condition(method_name, value=val)
            all_conditions_met = all_conditions_met and current_condition
            if not all_conditions_met:
                break

        return all_conditions_met

    def get_definition(self):
        """
        Creates a save-able form of Condition's data
        :rtype: list
        """
        def_list = []

        for entry in self.checks:
            cond_def = {'LABEL': entry['COMPONENT_LABEL'], 'METHOD': entry['METHOD'], 'VALUE': entry['VALUE']}
            def_list.append(cond_def)

        return def_list


class Effect(object):
    """
    Class which controls all actions, such as changing a Component's state
    """
    def __init__(self, actions):
        """
        :type actions: list
        """
        self.actions = actions

    def __str__(self):
        return str(self.actions)

    def get_definition(self):
        """
        Save-able representation of this Effect
        ":rtype: list
        """
        effect_def = []

        for entry in self.actions:
            effect_def.append({'METHOD': entry['METHOD_NAME'], 'LABEL': entry['LABEL'], 'ARG': entry['ARG']})

        return effect_def

    def perform_actions(self):
        """
        Method which does the stuff
        """

        for entry in self.actions:
            method = entry["METHOD"]
            arg = entry["ARG"]
            print(method)
            print(arg)
            if arg is None:
                method()
            else:
                method(arg)


def create_events(all_components, events_json_str='', events_list=None):
    """
    takes the raw string json from the server and parses it out to make new events
    :type all_components: list[Component]
    :param events_json_str: optional json of already-made events
    :param events_list: optional list of already-made events dict, must have one or the other
    :rtype: list[Event]
    """
    if events_list is None and events_json_str != '':
        events_list = json.loads(events_json_str)

    events = []

    for event in events_list:
        label = event['LABEL']
        condition = create_condition(event['CONDITIONS'], all_components)
        effect = create_effect(event['EFFECTS'], all_components)

        activate_condition = None
        deactivate_condition = None
        if 'ACTIVATE' in event:
            activate_condition = create_condition(event['ACTIVATE'], all_components)
        if 'DEACTIVATE' in event:
            deactivate_condition = create_condition(event['DEACTIVATE'], all_components)

        new_event = Event(label, condition, effect, activate_condition, deactivate_condition)
        events.append(new_event)

    return events


def create_effect(actions_list, all_components):
    """
    Creates an Effect out of a list of actions
    :param actions_list: list of actions to perform in Effect
            Format looks like this
                [ { 'LABEL':'component_label',
                    'METHOD':component_method_pointer,
                    'METHOD_NAME': 'method_string',
                    'ARG':optional_parameter }, ... ]
    :type all_components: list[Component]
    :rtype: Effect
    """
    actions = []

    for entry in actions_list:
        component_label = entry['LABEL']
        component = None
        for comp in all_components:
            # find the correct component based off its label, then quit looking
            if comp.get_label() == component_label:
                component = comp
                break
        # label doesn't represent an actual component
        if component is None:
            break
        method_name = entry['METHOD']
        arg = None
        if 'ARG' in entry:
            arg = entry['ARG']
        effect_method = component.effect_methods[method_name]
        actions.append({'METHOD': effect_method, 'ARG': arg, 'LABEL': component_label, 'METHOD_NAME': method_name})

    return Effect(actions)


def create_condition(checks_list, all_components_list):
    """
    Function to create a Condition from a list of checks
    :param checks_list: list of checks to perform
                format:[ {  'LABEL': 'component_label',
                            'METHOD': boolean-evaluating method which checks state of component,
                            'VALUE': value to compare against or general parameter for method
                        }, ... ]
    :type all_components_list: list[Component]
    :rtype: Condition
    """
    checks = []

    for entry in checks_list:
        component_label = entry['LABEL']
        component = None
        for comp in all_components_list:
            if comp.get_label() == component_label:
                component = comp
                break
        if component is None:
            break
        operator = entry['METHOD']
        value = entry['VALUE']

        # cast values to appropriate type
        comp_type = component.COMPONENT_TYPE
        if comp_type == 'COUNTER':
            value = int(value)
        elif comp_type == 'TIMER' or comp_type == 'ANALOG_INPUT':
            value = float(value)

        checks.append({'COMPONENT': component, 'COMPONENT_LABEL': component.get_label(),
                           'METHOD': operator, 'VALUE': value})

    return Condition(checks)
