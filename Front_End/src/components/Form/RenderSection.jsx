import React from "react";
import { FieldBody } from "./FieldBodys/FieldBody";
import { Grid, Row, Button, Glyphicon } from "react-bootstrap";
import { Header } from "./Header/Header";

export const RenderSection = ({
  fields,
  fieldName,
  inputdata,
  headerRow,
  pageName
}) => {
  let section = fields.map((field, index) => {
    return (
      <FieldBody
        fields={fields}
        field={field}
        inputdata={inputdata}
        id={index}
        key={field + index}
        pageName={pageName}
      />
    );
  });
  const { name, check = null, input = null, value = null } = headerRow;
  return (
    <Grid style={{ marginBottom: "50px", marginTop: "50px" }}>
      <Row>
        <h2>{fieldName}</h2>
      </Row>
      <Header
        pageName={pageName}
        name={name}
        input={input}
        check={check}
        value={value}
      />
      {section}
      <Row>
        <Button type="button" onClick={() => fields.push({})} block>
          <Glyphicon glyph="plus" /> Add field
        </Button>
      </Row>
    </Grid>
  );
};
