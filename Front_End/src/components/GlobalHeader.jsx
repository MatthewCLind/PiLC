import React, { Component } from "react";
import { Nav, Navbar, NavItem } from "react-bootstrap";
import { Switch, Route } from "react-router-dom";
import { LinkContainer } from "react-router-bootstrap";
import { withRouter } from "react-router-dom";

import { Components } from "./ComponentsPage";
import LiveFeed from "./LiveFeed";
import { Events } from "./EventsPage";

class GlobalHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <div>
        <Navbar inverse collapseOnSelect fixedTop>
          <Navbar.Header>
            <Navbar.Brand>PiLC-Prototype</Navbar.Brand>
            <Navbar.Toggle />
          </Navbar.Header>
          <Navbar.Collapse>
            <Nav pullRight>
              <LinkContainer to="/components">
                <NavItem eventKey={1}>Components</NavItem>
              </LinkContainer>
              <LinkContainer to="/events">
                <NavItem eventKey={2}>Events</NavItem>
              </LinkContainer>
                {/*<LinkContainer to="/livefeed">
                <NavItem eventKey={3}>Live Feed</NavItem>
              </LinkContainer>*/}
            </Nav>
          </Navbar.Collapse>
        </Navbar>
        <RoutingPaths />
      </div>
    );
  }
}

const RoutingPaths = () => (
  <Switch>
    <Route path="/components" component={Components} />
    <Route path="/events" component={Events} />
    {/*<Route path="/livefeed" component={LiveFeed} />*/}
  </Switch>
);

export default withRouter(GlobalHeader);
