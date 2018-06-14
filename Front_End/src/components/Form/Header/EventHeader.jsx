import React from "react";
import { Col, Row, Well } from "react-bootstrap";

export const EventHeader = ({ name, check, value }) => (
  <Row style={{ marginBottom: "0px", fontSize: "1.5em" }}>
    <Col xs={4} style={{ padding: "0px"}}>
    <Well style={{ marginBottom: "0px" }} bsSize="small">
        {name}
      </Well>
    </Col>
    <Col xs={4} style={{ padding: "0px" }}>
      <Well style={{ marginBottom: "0px" }} bsSize="small">
        {check}
      </Well>
    </Col>
    <Col xs={4} style={{ padding: "0px" }}>
      <Well style={{ marginBottom: "0px" }} bsSize="small">
        {value}
      </Well>
    </Col>
  </Row>
);

export default EventHeader;