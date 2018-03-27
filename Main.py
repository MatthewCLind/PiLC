import time
import FileHandler

# start off by getting saved data
all_components = FileHandler.load_components_definition()
all_events = FileHandler.load_events_definition(all_components)

# or wait for the first data from the client
while all_components is None or all_events is None:
    all_components = FileHandler.load_client_updates(all_components)

# live_feed.json, current_components.json, and current_events.json are all temp files
# they must be loaded when Main begins
FileHandler.save_live_feed(all_components)
FileHandler.send_client_components(all_components)
FileHandler.send_client_events(all_events)

# timer for next update
next_update = 0.0
UPDATE_PERIOD = 2

# timer for next live_feed write
next_live_feed = 0.0
LIVE_FEED_PERIOD = 1

# how fast the loop should run
LOOP_PERIOD = 0.1


while True:
    # Start off by handling timed file management
    if next_update < time.time():
        new_components, new_events = FileHandler.load_client_updates(all_components)

        new_c = new_components is not None
        new_e = new_events is not None

        # make sure the client-facing files always have the latest and greatest
        if new_c:
            all_components = new_components
            FileHandler.send_client_components(all_components)
        if new_e:
            all_events = new_events
            FileHandler.send_client_events(all_events)

        # only save definitions if there's something new
        # otherwise, frequent writes will jack up the SD card
        if new_c or new_e:
            FileHandler.save_definition(all_components, all_events)

        next_update = time.time() + UPDATE_PERIOD

    if next_live_feed < time.time():
        FileHandler.save_live_feed(all_components)
        next_live_feed = time.time() + LIVE_FEED_PERIOD

    # And now, for the event you've all been waiting for!
    try:
        for event in all_events:
            event.evaluate()

    # there may not have been any events in the file, so we got to wait
    except TypeError:
        pass
    except Exception as e:
        with open('error_log.txt', 'w') as f:
            err = 'Something went wrong while evaluating events.\n'
            err += e.message
            f.write(err)
        raise e

    time.sleep(LOOP_PERIOD)
