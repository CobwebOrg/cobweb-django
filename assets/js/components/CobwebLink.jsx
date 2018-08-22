import React from "react";

function CobwebLink(props) {
  console.log(props)
  return <a href={props.url}>{props.name}</a>;
}

export default CobwebLink;
