import { GlobalActions } from "../actions";

let initialState = {
  initialEventData: [],
  initialComponentData: [],
  eventOptions: [],
  formData: [],
  components: {},
  componentPageMessage: null,
  eventPageMessage: null
};

export default (state = initialState, action) => {
  switch (action.type) {
    case GlobalActions.Types.FetchInitialDataSuccess:
      const { initialData, name } = action.payload;
      if (name === "events") {
        return { ...state, initialEventData: initialData };
      } else if (name === "components") {
        return { ...state, initialComponentData: initialData };
      }
      return state;
    case GlobalActions.Types.AddEvent:
      if (action.payload.success) {
        const { event } = action.payload;
        return {
          ...state,
          formData: [...state.formData, ...state.initialEventData],
          eventOptions: [...state.eventOptions, event]
        };
      }
      return state;
    case GlobalActions.Types.DeleteEvent:
      const { id } = action.payload;
      return {
        ...state,
        formData: state.formData
          .slice(0, id)
          .concat(state.formData.slice(id + 1, state.formData.length)),
        eventOptions: state.eventOptions
          .slice(0, id)
          .concat(state.eventOptions.slice(id + 1, state.eventOptions.length))
      };
    case GlobalActions.Types.SetEventComponents:
      let { components } = action.payload;
      return {
        ...state,
        components
      };
    case GlobalActions.Types.SetFormMessage:
      let { hasErrors, page } = action.payload;
      let componentPageMessage = null;
      let eventPageMessage = null;
      if (hasErrors && page === "components") {
        componentPageMessage = "Please fill out all the fields.";
      } else if (!hasErrors && page === "components") {
        componentPageMessage = null;
      } else if (hasErrors && page === "events") {
        eventPageMessage = "Please fill out all the fields.";
      } else if (!hasErrors && page === "events") {
        eventPageMessage = null;
      }
      return {
        ...state,
        componentPageMessage,
        eventPageMessage
      };
    default:
      return state;
  }
};
