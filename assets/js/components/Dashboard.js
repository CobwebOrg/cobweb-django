import React, { Component } from "react";
import DashUserInfo from "./DashUserInfo";

import PropTypes from "prop-types";


class Dashboard extends Component {
  constructor(props) {
      super(props);
      this.state = {
        user: {
            name: 'Lindsay Deal',
            affiliations: [
              {name: 'Harvard University Library',
               url:  '/org/12'},
              {name: 'The Cobweb Organization',
               url:  '/org/21'}
            ],
            last_login: 'May 22, 2018'
        }
      };
  }

  render() {
    return <DashUserInfo user={this.state.user} />;
  }
}
export default Dashboard;