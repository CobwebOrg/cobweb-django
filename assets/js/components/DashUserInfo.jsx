import React, { Component, Div } from "react";

import PropTypes from "prop-types";


function OrganizationList(props) {
    return props.orgs.map((org) =>
            <div key={org.url}>
                <a href={org.url} class="text-user-dark">
                    {org.name}
                </a>
            </div>
    );
}


class DashUserInfo extends Component {

  render() {
    return (
        <div class="col-3 p-3">
            <div class="border p-4">
                <h1 class="mb-1 text-user-dark">{this.props.user.name}</h1>
                <OrganizationList orgs={this.props.user.affiliations} />
                <p class="mt-1 mb-4 text-user-dark">Last login: {this.props.user.last_login}</p>

                <table>
                    <tr><td class="pr-2">Replies to notes:</td><td>0</td></tr>
                    <tr><td class="pr-2">New notes:</td><td>2</td></tr>
                    <tr><td class="pr-2">Activity alerts:</td><td>5</td></tr>
                </table>
            </div>
        </div>
    );
  }
}
export default DashUserInfo;