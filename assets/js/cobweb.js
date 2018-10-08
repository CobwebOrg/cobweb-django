var $ = require("jquery");
import React from "react";
import ReactDOM from "react-dom";
import Dashboard from "./components/Dashboard";
import Resource from "./components/Resource";
import 'bootstrap';
// import '../scss/cobweb.scss';
import fontawesome from '@fortawesome/fontawesome';
import solid from '@fortawesome/fontawesome-free-solid';

import Select from 'react-select';

fontawesome.library.add(solid);

// Enable tooltips and popovers

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
});

$(function () {
  $('[data-toggle="popover"]').popover()
});

window.$$ = $; // Expose *this* jquery to browser console - $ gets overloaded
window.Dashboard = Dashboard;
window.ReactDOM = ReactDOM;
window.React = React;
window.components = {
  Resource: Resource,
  Select: Select
};