import React from "react";
import { Col, Row, Well } from "react-bootstrap";

export const ComponentHeader = ({ name, input }) => (
  <Row style={{ marginBottom: "0px", fontSize: "1.5em" }}>
    <Col xs={6} style={{ padding: "0px" }}>
      <Well style={{ marginBottom: "0px" }} bsSize="small">
        {name}
      </Well>
    </Col>
    <Col xs={6} style={{ padding: "0px" }}>
      <Well style={{ marginBottom: "0px" }} bsSize="small">
        {input}
      </Well>
    </Col>
  </Row>
);

export default ComponentHeader;