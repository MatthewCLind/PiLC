import React from "react";
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

export const ComponentFieldBody = ({ fields, field, id, inputdata }) => (
  <Row style={{ marginBottom: "0px" }}>
    <FormGroup controlId={field + id}>
      <Col xs={6} style={{ padding: "0px" }}>
        <Field
          name={`${field}.inputOne`}
          inputdata={inputdata[0]}
          componentClass={inputdata[0].name}
          component={RenderInput}
        />
      </Col>
      <Col xs={6} style={{ padding: "0px" }}>
        <InputGroup>
          <Field
            name={`${field}.inputTwo`}
            inputdata={inputdata[1]}
            componentClass={inputdata[1].name}
            component={RenderInput}
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
