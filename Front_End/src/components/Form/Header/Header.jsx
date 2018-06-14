import React from "react";
import { ComponentHeader } from "./ComponentHeader";
import { EventHeader } from "./EventHeader";

export const Header = ({
  pageName,
  name,
  check = null,
  value = null,
  input = null
}) => {
  if (pageName === "components") {
    return <ComponentHeader name={name} input={input} />;
  } else {
    return <EventHeader name={name} check={check} value={value} />;
  }
};
