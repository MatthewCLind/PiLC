import React from "react";
import { FormControl } from "react-bootstrap";

export const TextInput = props => (
  <div>
    <FormControl {...props.input} {...props} />
  </div>
);
