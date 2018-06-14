import React from "react";
import PropTypes from "prop-types";
import { Grid, Button, ButtonGroup, Row, Alert } from "react-bootstrap";
import { Form } from "../Form/Form";
import { AddEventModal } from "./AddEventModal";
import { DeleteEventModal } from "./DeleteEventModal";
import "react-widgets/dist/css/react-widgets.css";
import DropdownList from "react-widgets/lib/DropdownList";

const EventsForm = ({
  formData,
  addEvent,
  deleteEvent,
  showEventModal,
  showDeleteEvent,
  openEventModal,
  openDeleteEvent,
  closeDeleteEvent,
  closeEventModal,
  eventOptions,
  subFormPage,
  handleEventChange,
  eventName,
  handleEventNameChange,
  eventPageMessage
}) => {
  return (
    <div>
      <Grid>
        {eventPageMessage && (
          <Row>
            <Alert bsStyle="warning">{eventPageMessage}</Alert>
          </Row>
        )}
        <Row>
          <Button
            bsStyle="primary"
            style={{ padding: "20px", fontSize: "1.5em" }}
            block
            type="submit"
          >
            Save Events
          </Button>
          <ButtonGroup justified>
            <ButtonGroup>
              <Button bsStyle="success" type="button" onClick={openEventModal}>
                Add Event
              </Button>
            </ButtonGroup>
            <ButtonGroup>
              <Button bsStyle="warning" type="button" onClick={openDeleteEvent}>
                Delete Event
              </Button>
            </ButtonGroup>
          </ButtonGroup>
          <DropdownList
            data={eventOptions}
            placeholder="Select Event"
            onChange={value => handleEventChange(value)}
            value={eventName}
          />
          <AddEventModal
            showEventModal={showEventModal}
            closeEventModal={closeEventModal}
            addEvent={addEvent}
            eventName={eventName}
            handleEventNameChange={handleEventNameChange}
          />
          <DeleteEventModal
            showDeleteEvent={showDeleteEvent}
            closeDeleteEvent={closeDeleteEvent}
            deleteEvent={deleteEvent}
          />
        </Row>
      </Grid>
      <Form formData={formData} name="events" subFormPage={subFormPage} />
    </div>
  );
};

EventsForm.propTypes = {
  formData: PropTypes.array,
  addEvent: PropTypes.func
};

export default EventsForm;
