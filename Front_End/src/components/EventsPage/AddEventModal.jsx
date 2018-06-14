import React from "react";
import PropTypes from "prop-types";
import {
  Modal,
  Button,
  ButtonGroup,
  FormGroup,
  FormControl,
  ControlLabel
} from "react-bootstrap";

const EventName = ({ eventName, handleEventNameChange }) => (
  <FormGroup controlId="eventName">
    <ControlLabel>Event Name</ControlLabel>
    <FormControl
      type="text"
      placeholder="Enter Event Name"
      value={eventName}
      onChange={handleEventNameChange}
    />
  </FormGroup>
);

export const AddEventModal = ({
  showEventModal,
  closeEventModal,
  addEvent,
  eventName,
  handleEventNameChange
}) => (
  <Modal show={showEventModal} onHide={closeEventModal}>
    <Modal.Header closeButton>
      <Modal.Title>Add an Event</Modal.Title>
    </Modal.Header>
    <Modal.Body>
      <EventName
        eventName={eventName}
        handleEventNameChange={handleEventNameChange}
      />
      <ButtonGroup vertical block>
        <Button bsStyle="success" type="button" onClick={addEvent}>
          Add Event
        </Button>
        <Button bsStyle="warning" type="button" onClick={closeEventModal}>
          Close
        </Button>
      </ButtonGroup>
    </Modal.Body>
  </Modal>
);

AddEventModal.propTypes = {
  showEventModal: PropTypes.bool,
  closeEventModal: PropTypes.func,
  addEvent: PropTypes.func
};
