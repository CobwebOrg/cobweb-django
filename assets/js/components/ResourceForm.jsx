import React from "react";
import CobwebLink from "./CobwebLink";
import { withFormik } from 'formik';

  
function FormField(props) {
  return (
    <div className="row form-group">
      <label className="col-md-3 col-form-label form-control-label">
        {props.label.charAt(0).toLocaleUpperCase() 
         + props.label.substr(1).replace('_', ' ')}
      </label>
      <div className="col-md">
        <input className="w-100" default={props.value} />
      </div>
    </div>
  );
}

// function SourceForm(props) {
//   const form_fields = Object.keys(props.formData).map((fieldName) =>
//     <FormField label={fieldName} key={fieldName}
//                value={props.formData[fieldName]} />
//   );
//   return (
//     <div className="form-section">
//       <h3>Submitted by <CobwebLink url={"/user/"+props.source} name={props.source}/></h3>
//     {form_fields}
//   </div>)
// }

// Our inner form component which receives our form's state and updater methods as props
const InnerResourceForm = ({
  values,
  errors,
  touched,
  handleChange,
  handleBlur,
  handleSubmit,
  isSubmitting,
}) => {
  const form_fields = Object.keys(values).map((fieldName) =>
    <FormField label={fieldName} key={fieldName}
               value={values[fieldName]} />
  );
  return (
    <form onSubmit={handleSubmit}>
      {form_fields}
      {/* <input
        type="title"
        name="title"
        onChange={handleChange}
        onBlur={handleBlur}
        value={values.title}
      />
      {touched.title && errors.title && <div>{errors.title}</div>}
      <input
        type="description"
        name="description"
        onChange={handleChange}
        onBlur={handleBlur}
        value={values.description}
      />
      {touched.description && errors.description && <div>{errors.description}</div>} */}
      <button type="submit" disabled={isSubmitting}>
        Submit
      </button>
    </form>
  );
}


const SourceForm = withFormik({
  mapPropsToValues: props => {
    const defaults = {
      title: '',
      description: ''
    };
    console.log(defaults, props)
    return Object.assign(defaults, props.formData);
  },

  validate: (values, props) => {
    const errors = {};
    // if (!values.email) {
    //   errors.email = 'Required';
    // }
    return errors;
  },

  handleSubmit: (values, rand_obj) => console.log(values, rand_obj)
})(InnerResourceForm);


class ResourceForm extends React.Component {
  constructor(props) {
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
    return source_forms;
  }
}

export default ResourceForm;