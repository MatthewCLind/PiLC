import React from "react";
import "react-widgets/dist/css/react-widgets.css";
import DropdownList from "react-widgets/lib/DropdownList";

export const SelectInput = ({ input, inputdata, options = [] }) => {
  const { valueField, textField, disabled = false } = inputdata;
  const { onChange } = input;
  return (
    <DropdownList
      {...input}
      data={options}
      valueField={valueField}
      textField={textField}
      onChange={onChange}
      disabled={disabled}
    />
  );
};
