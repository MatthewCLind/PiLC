import React, { Component } from "react";
import { Form as BootStrapForm, Grid } from "react-bootstrap";
import EventsForm from "./EventsForm";
import { reduxForm } from "redux-form";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { GlobalActions } from "../../actions";

const validate = formValues => {
  let errors = false;
  let section = Object.entries(formValues);
  if (section.length === 0) {
    errors = true;
  }
  section.forEach(values => {});
  return errors;
};

class Events extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showEventModal: false,
      showDeleteEvent: false,
      subFormPage: null,
      eventName: ""
    };
  }

  submit = values => {
    let page = "events";
    let formErrors = validate(values);
    this.props.setFormMessage(formErrors, page);
    let jsonObject = 
    {
      COMPONENTS: {},
      EVENTS: []
    };
    console.log('values', values);
    Object.entries(values).forEach(([k, v]) => {
      if (k.includes("components")) 
      {
        let component_type = k.substring(k.indexOf("-") + 2);
        jsonObject["COMPONENTS"][component_type] = v;
      } 
      else 
      {
        let index = k.substring(
          k.indexOf(" ") + 1,
          k.indexOf(" ", k.indexOf(" ") + 1)
        );
        let sectionName = k.substring(k.indexOf("-") + 2);
        let sectionValue = {
          [sectionName]: v
        };
        jsonObject["EVENTS"][index] = {
          LABEL:this.props.eventOptions[index],
          ...jsonObject["EVENTS"][index],
          ...sectionValue
        };
      }
    });
    console.log(jsonObject);
    // NOTE: modify this function with your post request
    this.submitFormData(jsonObject);
  };

  componentDidMount = () => {
    this.props.fetchInitialData("http://localhost:3001/events/", "events");
    console.log("Initial load props: ", this.props);
    console.log("Initial load state: ", this.state);
  };

  handleAddEvent = () => {
    this.props.addEvent(`${this.state.eventName}`);
    this.setState({
      showEventModal: false,
      eventName: ""
    });
  };

  handleDeleteEvent = () => {
    this.props.deleteEvent(this.state.subFormPage);
    this.setState({
      showDeleteEvent: false,
      eventName: "",
      subFormPage: null
    });
  };

  handleCloseEventModal = () => {
    this.setState({ showEventModal: false });
  };

  handleOpenEventModal = () => {
    this.setState({ showEventModal: true });
  };

  handleOpenDeleteEvent = () => {
    this.setState({ showDeleteEvent: true });
  };

  handleCloseDeleteEvent = () => {
    this.setState({ showDeleteEvent: false });
  };

  handleEventChange = event => {
    this.setState({
      eventName: event,
      subFormPage: this.props.eventOptions.findIndex(option => option === event)
    });
  };

  handleEventNameChange = e => {
    this.setState({ eventName: e.target.value });
  };

  submitFormData(values) {
    let request = "http://localhost:3001/dataEvents/1";// + this.state.eventName;
    fetch(request, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      },
      method: "PUT",
      body: JSON.stringify(values)
    });
  }
  render() {
    // NOTE: component props
    const { handleSubmit } = this.props;
    // NOTE: reducer props
    const { eventOptions, formData, eventPageMessage } = this.props;
    return (
      <Grid style={{ marginTop: "100px" }}>
        <BootStrapForm onSubmit={handleSubmit(this.submit)}>
          <EventsForm
            formData={formData}
            subFormPage={this.state.subFormPage}
            addEvent={this.handleAddEvent}
            deleteEvent={this.handleDeleteEvent}
            showEventModal={this.state.showEventModal}
            showDeleteEvent={this.state.showDeleteEvent}
            openEventModal={this.handleOpenEventModal}
            openDeleteEvent={this.handleOpenDeleteEvent}
            closeDeleteEvent={this.handleCloseDeleteEvent}
            closeEventModal={this.handleCloseEventModal}
            eventOptions={eventOptions}
            handleEventChange={this.handleEventChange}
            eventName={this.state.eventName}
            handleEventNameChange={this.handleEventNameChange}
            eventPageMessage={eventPageMessage}
          />
        </BootStrapForm>
      </Grid>
    );
  }
}

const mapStateToProps = state => {
  return {
    ...state.global
  };
};

const mapDispatchToProps = dispatch => {
  const {
    fetchInitialData,
    addEvent,
    deleteEvent,
    setFormMessage
  } = GlobalActions;
  return bindActionCreators(
    { fetchInitialData, addEvent, deleteEvent, setFormMessage },
    dispatch
  );
};

Events = connect(mapStateToProps, mapDispatchToProps)(Events);

// Decorate the form component
export default reduxForm({
  form: "piLC",
  destroyOnUnmount: false, // <------ preserve form data
  forceUnregisterOnUnmount: true
})(Events);
