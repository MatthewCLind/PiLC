import React from "react";
import { SelectInput } from "./SelectInput";
import { TextInput } from "./TextInput";
import { TimerInput } from "./TimerInput";
import { NumberInput } from "./NumberInput";

export const RenderInput = props => {
  const { componentClass = "select" } = props;
  switch (componentClass) {
    case "select":
      return <SelectInput {...props} />;
    case "input":
      return <TextInput {...props} />;
    case "timer":
      return <TimerInput {...props} />;
    case "number":
      return <NumberInput {...props} />;
    default:
      return null;
  }
};
