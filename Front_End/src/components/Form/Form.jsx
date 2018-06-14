import React from "react";
import { FieldArray } from "redux-form";
import { RenderSubForm } from "./RenderSubForm";
import PropTypes from "prop-types";

export const Form = ({ formData, name, subFormPage = null }) => {
  let form = formData.map((subFormData, index) => {
    if (subFormPage === index || name === "components") {
      return (
        <FieldArray
          key={index}
          name={`${name} ${index}`}
          subFormName={`${name} ${index} - `}
          subFormData={subFormData}
          component={RenderSubForm}
          pageName={name}
        />
      );
    }
    return null;
  });
  return form;
};

Form.propTypes = {
  formData: PropTypes.array,
  name: PropTypes.string,
  subFormPage: PropTypes.number
};
