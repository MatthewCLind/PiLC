import React, { Component } from "react";
import {
  FormGroup,
  Col,
  Row,
  InputGroup,
  Button,
  Glyphicon
} from "react-bootstrap";
import { RenderInput } from "../inputs/RenderInput";
import { Field } from "redux-form";
import { connect } from "react-redux";
import { conditions } from "./fields";
import { reduxForm } from "redux-form";

class EventFieldBody extends Component {
  render() {
    const { fields, field, id, inputdata, components } = this.props;
    let componentClass = [];
    let boundaries = [];
    let sectionNames = ["Conditions", "Effects", "Activate", "Deactivate"];
    let sectionName = sectionNames.find(
      name => (fields.name.includes(name) ? name : null)
    );

    let checksActions = sectionName !== "Effects" ? "checks" : "actions";

    // Populate components select input with options from component page
    let optionsLabels = Object.values(components).reduce((acc, curr) => {
      curr.forEach(val => acc.push(val.inputOne));
      return acc;
    }, []);
    let options = [];
    options[0] = optionsLabels;

    // Populate Check/Change select input with options from components inputs
    let condFieldsData = Object.entries(conditions);
    let compInputs = fields.getAll();
    let compData = Object.entries(components).find(comp => {
      return comp[1][0].inputOne === compInputs[id].inputOne;
    });
    let conditionIndex = -1;

    if (compData) {
      let record = Object.entries(conditions).find(condition =>
        compData[0].includes(condition[0])
      );
      options[1] = record[1][`${checksActions}Options`];
      conditionIndex = condFieldsData.findIndex(condition =>
        compData[0].includes(condition[0])
      );
    }
    if (compInputs[id].inputOne && compInputs[id].inputTwo) {
      Object.entries(condFieldsData[conditionIndex][1][checksActions]).find(
        ([k, v]) => {
          if (
            k === compInputs[id].inputTwo &&
            compData[1][0].inputOne === compInputs[id].inputOne
          ) {
            componentClass[2] = v.input;
            if (v.input === "number") {
              boundaries[2] = {
                min: v.min,
                max: v.max
              };
            }
            if (v.input === "select") {
              options[2] = v.options;
            }
          }
        }
      );
    }
    return (
      <Row style={{ marginBottom: "0px" }}>
        <FormGroup controlId={field + id}>
          <Col xs={4} style={{ padding: "0px" }}>
            <Field
              name={`${field}.inputOne`}
              inputdata={inputdata[0]}
              componentClass={componentClass[0]}
              component={RenderInput}
              options={options[0]}
              boundaries={boundaries[0]}
              // disabled={disabled[0]}
            />
          </Col>
          <Col xs={4} style={{ padding: "0px" }}>
            <Field
              name={`${field}.inputTwo`}
              inputdata={inputdata[1]}
              componentClass={componentClass[1]}
              component={RenderInput}
              options={options[1]}
              boundaries={boundaries[1]}
              // disabled={disabled[1]}
            />
          </Col>
          <Col xs={4} style={{ padding: "0px" }}>
            <InputGroup>
              <Field
                name={`${field}.inputThree`}
                inputdata={inputdata[2]}
                componentClass={componentClass[2]}
                component={RenderInput}
                options={options[2]}
                boundaries={boundaries[2]}
                // disabled={disabled[2]}
              />
              <InputGroup.Button>
                <Button onClick={() => fields.remove(id)}>
                  <Glyphicon glyph="remove" />
                </Button>
              </InputGroup.Button>
            </InputGroup>
          </Col>
        </FormGroup>
      </Row>
    );
  }
}

const mapStateToProps = state => {
  return {
    ...state.global
  };
};

const mapDispatchToProps = dispatch => {};

EventFieldBody = connect(mapStateToProps, mapDispatchToProps)(EventFieldBody);

// Decorate the form component
export default reduxForm({
  form: "piLC",
  destroyOnUnmount: false, // <------ preserve form data
  forceUnregisterOnUnmount: true
})(EventFieldBody);
