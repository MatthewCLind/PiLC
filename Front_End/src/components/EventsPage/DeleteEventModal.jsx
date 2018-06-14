import React from "react";
import PropTypes from "prop-types";
import { Modal, Button, ButtonGroup } from "react-bootstrap";

export const DeleteEventModal = ({
  showDeleteEvent,
  closeDeleteEvent,
  deleteEvent
}) => (
  <Modal show={showDeleteEvent} onHide={closeDeleteEvent}>
    <Modal.Header closeButton>
      <Modal.Title>Delete an Event</Modal.Title>
    </Modal.Header>
    <Modal.Body>Are you sure?</Modal.Body>
    <Modal.Footer>
      <ButtonGroup vertical block>
        <Button bsStyle="danger" type="button" onClick={deleteEvent}>
          Delete Event
        </Button>
        <Button onClick={closeDeleteEvent}>Close</Button>
      </ButtonGroup>
    </Modal.Footer>
  </Modal>
);

DeleteEventModal.propTypes = {
  showDeleteEvent: PropTypes.bool,
  closeDeleteEvent: PropTypes.func,
  deleteEvent: PropTypes.func
};
