export const Types = {
  AddEvent: "EVENTS_ADD_EVENT",
  DeleteEvent: "EVENTS_DELETE_EVENT",
  FetchInitialDataSuccess: "FETCH_INITIAL_DATA_SUCCESS",
  SetEventComponents: "COMPONENTS_SET_EVENT_COMPONENTS",
  SetFormMessage: "SET_FORM_MESSAGE"
};

export function addEvent(event) {
  return dispatch =>
    dispatch({
      type: Types.AddEvent,
      payload: {
        success: true,
        event
      }
    });
}

export function deleteEvent(id) {
  return dispatch =>
    dispatch({
      type: Types.DeleteEvent,
      payload: {
        id
      }
    });
}

export function fetchInitialData(url, name) {
  return dispatch => {
    fetch(url)
      .then(response => {
        if (!response.ok) {
          throw Error(response.statusText);
        }
        return response;
      })
      .then(response => response.json())
      .then(response => dispatch(fetchInitialDataSuccess(response, name)))
      .catch(err => console.log(err));
  };
}

export function fetchInitialDataSuccess(initialData, name) {
  return dispatch =>
    dispatch({
      type: Types.FetchInitialDataSuccess,
      payload: {
        initialData,
        name
      }
    });
}

export function setEventComponents(components) {
  return dispatch =>
    dispatch({
      type: Types.SetEventComponents,
      payload: {
        components
      }
    });
}

export function setFormMessage(hasErrors, page) {
  return dispatch =>
    dispatch({
      type: Types.SetFormMessage,
      payload: {
        hasErrors,
        page
      }
    });
}
