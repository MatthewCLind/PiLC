import React from "react";
import { FieldArray } from "redux-form";
import { RenderSection } from "./RenderSection";
import PropTypes from "prop-types";

export const RenderSubForm = ({ fields, subFormData, subFormName, pageName }) => {
  let subForm = subFormData.map((section, index) => {
    return (
      <FieldArray
        key={index}
        name={`${subFormName}${section.sectionName}`}
        fieldName={section.sectionName}
        headerRow={section.headerRow}
        inputdata={section.inputdata}
        component={RenderSection}
        pageName={pageName}
        // validate={[required]}
      />
    );
  });
  return subForm;
};

RenderSubForm.propTypes = {
  subFormData: PropTypes.array,
  subFormName: PropTypes.string
};
