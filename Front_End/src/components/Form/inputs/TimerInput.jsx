import React from "react";
import "rc-time-picker/assets/index.css";
import TimePicker from "rc-time-picker";
import moment from "moment";

export const TimerInput = ({ input: { onChange, value } }) => {
  return (
    <TimePicker
      popupClassName="popup"
      onChange={onChange}
      date={false}
      value={!value ? null : moment(value)}
    />
  );
};
