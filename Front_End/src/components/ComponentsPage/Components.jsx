import React, { Component } from "react";
import { Form as BSForm, Grid, Button, Row, Alert } from "react-bootstrap";
import { Form } from "../Form/Form";
import { reduxForm } from "redux-form";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { GlobalActions } from "../../actions";

const validate = formValues => {
  let errors = false;
  let section = Object.entries(formValues);
  section.forEach(values => {
    if (values[0].includes("components")) {
      values[1].forEach(row => {
        if (!row.hasOwnProperty("inputOne") || !row.hasOwnProperty("inputTwo")) {
          errors = true;
        }
      });
    }
  });
  return errors;
};

class Components extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  submit = values => {
    let page = "components";
    let components = Object.entries(values).reduce((acc, curr) => {
      if (curr[0].includes("components")) {
        acc[curr[0].replace("components 0 -  ", "")] = curr[1];
      }
      return acc;
    }, {});
    let formErrors = validate(values);
    if (!formErrors) {
      this.props.setEventComponents(components);
    }
    this.props.setFormMessage(formErrors, page);
  };

  componentDidMount() {
    this.props.fetchInitialData(
      "http://localhost:3001/components/",
      "components"
    );
  }

  submitFormData(values) {
    var post = values;
    let request = "http://localhost:3001/dataComponents";
    fetch(request, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      },
      method: "PUT",
      
      body: JSON.stringify(post)
    })
  }

  render() {
    // NOTE: component props
    const { handleSubmit } = this.props;
    // NOTE: reducer props
    const { initialComponentData, componentPageMessage } = this.props;
    return (
      <Grid style={{ marginTop: "100px" }}>
        <BSForm onSubmit={handleSubmit(this.submit)}>
          <Grid>
            {componentPageMessage && (
              <Row>
                <Alert bsStyle="warning">{componentPageMessage}</Alert>
              </Row>
            )}
            <Row>
              <Button
                bsStyle="primary"
                style={{ padding: "20px", fontSize: "1.5em" }}
                onClick = {() => this.submitFormData(this.props.components)}
                block
                type="submit"
              >
                Submit Components
              </Button>
            </Row>
          </Grid>
          <Form
            formData={initialComponentData}
            name="components"
            subFormPage={0}
          />
        </BSForm>
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
    setEventComponents,
    setFormMessage
  } = GlobalActions;
  return bindActionCreators(
    { fetchInitialData, setEventComponents, setFormMessage },
    dispatch
  );
};

Components = connect(mapStateToProps, mapDispatchToProps)(Components);

// Decorate the form component
export default reduxForm({
  form: "piLC",
  validate,
  destroyOnUnmount: false, // <------ preserve form data
  forceUnregisterOnUnmount: true
})(Components);
