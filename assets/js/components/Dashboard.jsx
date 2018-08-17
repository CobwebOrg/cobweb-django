import React, { Component } from "react";
import DashUserInfo from "./DashUserInfo";
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import ReactTable from "react-table";

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
        },
        data:{
          projects: [
            {
              "id":"projects.project.1",
              "django_ct":"projects.project",
              "django_id":"1",
              "title":"Open nominations project.",
              "nomination_policy":"Open",
              "status":"Active",
              "impact_factor":1,
              "unclaimed_nominations":2,
              "claimed_nominations":1,
              "held_nominations":0,
              "_version_":1601459063415111680},
            {
              "id":"projects.project.2",
              "django_ct":"projects.project",
              "django_id":"2",
              "title":"Milton, Massachusetts",
              "description":"Milton, Massachusetts is lovely in fall.",
              "nomination_policy":"Restricted",
              "status":"Inactive",
              "impact_factor":0,
              "unclaimed_nominations":1,
              "claimed_nominations":0,
              "held_nominations":0,
              "_version_":1601459063417208832},
            {
              "id":"projects.project.3",
              "django_ct":"projects.project",
              "django_id":"3",
              "title":"Mount Holyoke College",
              "nomination_policy":"Open",
              "status":"Active",
              "impact_factor":0,
              "unclaimed_nominations":1,
              "claimed_nominations":0,
              "held_nominations":0,
              "_version_":1601459063417208833},
            {
              "id":"projects.project.4",
              "django_ct":"projects.project",
              "django_id":"4",
              "title":"Hague, New York",
              "description":"Hague, New York, is a small town located in Adirondack Park on the western shore on the northern end of beautiful Lake George.  It is home to the family-friendly Northern Lake George Yacht Club and Roger's Rock.  Not much else, though.  Indian Kettles is pretty cool, but it is private property, so it's been years since anyone has seen the actual kettles.  Most of Hague overlooks Anthony's Nose, which is quite beautiful.  Silver Bay may also be within the town's borders, I'm not sure.  Hague desperately needs a restaurant that serves at least a couple of vegetarian options, though.",
              "nomination_policy":"Restricted",
              "status":"Active",
              "impact_factor":0,
              "unclaimed_nominations":0,
              "claimed_nominations":0,
              "held_nominations":0,
              "_version_":1601459063417208834},
            {
              "id":"projects.project.5",
              "django_ct":"projects.project",
              "django_id":"5",
              "title":"Dodging the memory hole project",
              "nomination_policy":"Open",
              "status":"Active",
              "impact_factor":0,
              "unclaimed_nominations":0,
              "claimed_nominations":0,
              "held_nominations":0,
              "_version_":1601459063418257408},
            {
              "id":"projects.project.6",
              "django_ct":"projects.project",
              "django_id":"6",
              "title":"Propaganda, disinformation, parody, dismissal: Making sense of \"Fake News\".",
              "description":"This project captures and categorizes online sources that purport to provide news coverage of current events.",
              "nomination_policy":"Public",
              "status":"Open",
              "impact_factor":2,
              "unclaimed_nominations":994,
              "claimed_nominations":1,
              "held_nominations":1,
              "_version_":1601459063421403136},
          ]
        }
      };
  }

  render() {

    return (
      <div class='row'>
        <DashUserInfo user={this.state.user} />
        <Tabs className="col-9 p-3" selectedTabClassName="active">
          
          <link rel="stylesheet" href="https://unpkg.com/react-table@latest/react-table.css" />
          <TabList className="nav-infotabs mb-4">
            <Tab className="nav-link">My Projects</Tab>
            <Tab className="nav-link">My Nominations</Tab>
            <Tab className="nav-link">My Claims</Tab>
            <Tab className="nav-link">My Holdings</Tab>
          </TabList>

          <TabPanel>
          <ReactTable data={this.state.data.projects}
                      columns={[{Header: 'Project', accessor: 'title'},
                                {Header: 'Unclaimed', accessor: 'unclaimed_nominations'},
                                {Header: 'Claimed', accessor: 'claimed_nominations'},
                                {Header: 'Held', accessor: 'held_nominations'}]}
                      showPaginationTop="True"
                      defaultPageSize="10" />

          </TabPanel>
          <TabPanel>
            <h2>Any content 2</h2>
          </TabPanel>
          <TabPanel>
            <h2>Any content 3</h2>
          </TabPanel>
          <TabPanel>
            <h2>Any content 4</h2>
          </TabPanel>
        </Tabs>
      </div>
    );
  }
}
export default Dashboard;