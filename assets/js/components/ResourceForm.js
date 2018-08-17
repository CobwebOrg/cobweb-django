import React from "react";

function ConsolidatedResourceForm(props) {
  
function FormField(props) {
  return (
    <div className="row form-group">
      <label className="col-md-3 col-form-label form-control-label">
        {props.label}
      </label>
      <div className="col-md">
        <input className="w-100" default={props.value} />
      </div>
    </div>
  );
}

function SourceForm(props) {
  const form_fields = Object.keys(props.formData).map((fieldName) =>
    <FormField label={fieldName} key={fieldName}
               value={props.formData[fieldName]} />
  );
  return <div className="form-section">
    <h3>submitted by {props.source}</h3>
    {form_fields}
  </div>
}

class ResourceForm extends React.Component {
  constructor(props) {
    console.log(props);
    super(props);
    this.state = {
      initial: props,
      value: 'Please write an essay about your favorite DOM element.'
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    alert('An essay was submitted: ' + this.state.value);
    event.preventDefault();
  }

  render() {
    const source_forms = Object.keys(this.state.initial).map((key) => 
      <SourceForm source={key} key={key} formData={this.state.initial[key]} />
    );
    return (
      <form onSubmit={this.handleSubmit}>
        {source_forms}
      </form>
    );
  }
}

export default ResourceForm;