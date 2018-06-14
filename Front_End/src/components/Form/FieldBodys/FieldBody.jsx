import React from "react";
import { ComponentFieldBody } from "./ComponentFieldBody";
import EventFieldBody from "./EventFieldBody";

export const FieldBody = props => {
  const { fields, field, id, inputdata, pageName } = props;
  if (pageName === "components") {
    return <ComponentFieldBody fields={fields} field={field} id={id} inputdata={inputdata} />
  }
  return <EventFieldBody fields={fields} field={field} id={id} inputdata={inputdata} />
};
