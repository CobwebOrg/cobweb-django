var $ = require("jquery");
import React from "react";
import ReactDOM from "react-dom";
import Dashboard from "./components/Dashboard";
import 'bootstrap';
// import '../scss/cobweb.scss';
import fontawesome from '@fortawesome/fontawesome';
import solid from '@fortawesome/fontawesome-free-solid';

fontawesome.library.add(solid);

// Make TextAreas auto-sizing

$('textarea').each(function () {
  this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
}).on('input', function () {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
});

window.$$ = $; // Expose *this* jquery to browser console - $ gets overloaded
window.Dashboard = Dashboard;
window.ReactDOM = ReactDOM;
window.React = React;
