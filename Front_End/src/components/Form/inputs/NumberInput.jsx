import React from "react";
import "react-widgets/dist/css/react-widgets.css";
import localizer from "react-widgets-simple-number";
import NumberPicker from "react-widgets/lib/NumberPicker";

export const NumberInput = ({
  input,
  inputdata,
  boundaries = { max: inputdata.max, min: inputdata.min }
}) => {
  localizer();
  const { min, max } = boundaries;
  let { onChange } = input;
  return <NumberPicker {...input} min={min} max={max} onChange={onChange} />;
};
