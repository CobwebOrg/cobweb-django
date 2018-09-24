import React from "react";
const _ = require("lodash");


// cf. https://werxltd.com/wp/2010/05/13/javascript-implementation-of-javas-string-hashcode-method/
String.prototype.hashCode = function(){
	var hash = 0;
	if (this.length == 0) return hash;
	for (var i = 0; i < this.length; i++) {
		var char = this.charCodeAt(i);
		hash = ((hash<<5)-hash)+char;
		hash = hash & hash; // Convert to 32bit integer
	}
	return hash;
}

class SourceButton extends React.Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    this.props.togglerCallback(this.props.source.url)
  }

  render() {
    return ([
      <span className={this.props.selected ? 'source-toggler selected' : 'source-toggler'}
            onClick={this.handleClick}>{this.props.source.name}</span>,
      <a href={this.props.source.url}>[view]</a>
    ]);
  }
}

function MDField({fieldName, values}) {
  if (values.length > 0) {
    var className = "datum";
    if (['title', 'description'].includes(fieldName)) {
      className += " datum-line";
    }
    if (['tags', 'subject_headings', 'subject'].includes(fieldName)) {
      className += " badge badge-info";
    }

    var valueObjects = values.map(
      v => <span className={className} key={v.hashCode()}>{v}</span>
    );

    return (
      <div className="row">
        <label className="col-3">{_.upperFirst(fieldName)}</label>
        <div className="col">{valueObjects}</div>
      </div>
    );
  } else {
    return null;
  }
}


function Metadata(props) {
  return (
    [...props.md_map.entries()].map(([fieldName, values]) => (
      <MDField fieldName={fieldName} key={fieldName} values={values} />
    ))
  );
}


class Resource extends React.Component {
  constructor(props) {
    super(props);
  
    this.state = {
      is_selected: new Map(
        [...props.resource.nominations, ...props.resource.imported_records]
        .map(x => [x.source.url, true])
      )
    };

    this.toggleSource = this.toggleSource.bind(this);
    this.mergedMD = this.mergedMD.bind(this);
    this.get_all_records = this.get_all_records.bind(this);
    this.get_selected_records = this.get_selected_records.bind(this);
  }

  get_all_records() {
    return [...this.props.resource.nominations,
            ...this.props.resource.imported_records];
  }

  get_selected_records() {
    return _.chain(this.get_all_records())
            .map(r => this.state.is_selected.get(r.source.url) ? r : null)
            .compact()
            .value();
  }

  mergedMD() {
    var records = this.get_selected_records();

    var keys = _.chain(records)
                .map(r => Object.keys(r.metadata))
                .flatten()
                .uniq()
                .value();

    var merged = new Map
    keys.forEach(key => {
      merged.set(
        key, 
        _.chain(records)
         .map(r => r.metadata[key])
         .flatten()
         .compact()
         .countBy(value => ((typeof value === 'string') ? value : value.name))
         .toPairs()
         .map(([value, n]) => ({value: value, n: n}))
         .sortBy('n')
         .reverse()
         .map(v => v.value)
         .value()
      );
    });
    return merged;
  }

  toggleSource(sourceURL) {
    var newState = this.state;
    newState.is_selected.set(sourceURL, !(this.state.is_selected.get(sourceURL)));
    this.setState((state, props) => newState);
  }

  render() {
    var source_selectors = [];
    if (this.props.resource.nominations) {
      source_selectors.push(...[
        <h3 key='nominations-h3'>Nominations</h3>,
        <ul>
          {this.props.resource.nominations.map(n => (
            <li key={n.source.url} href={n.source.url}>
              <SourceButton togglerCallback={this.toggleSource} source={n.source} 
                            selected={this.state.is_selected.get(n.source.url)} />
            </li>
          ))}
        </ul>
      ]);
    }
    if (this.props.resource.imported_records) {
      source_selectors.push(...[
        <h3 key='imported_records-h3'>External Holdings</h3>,
        <ul>
          {this.props.resource.imported_records.map(n => (
            <li key={n.source.url} href={n.source.url}>
              <SourceButton togglerCallback={this.toggleSource} source={n.source} 
                            selected={this.state.is_selected.get(n.source.url)} />
            </li>
          ))}
        </ul>
      ]);
    }

    return [
      <h2 className="mt-1 mb-3">Resource URL: {this.props.resource.url}</h2>,

      <div className="row">
        <div className="col-3">{source_selectors}</div>
        <div className="col">
          <Metadata md_map={this.mergedMD()} />
        </div>
      </div>
    ];
  }
}

export default Resource;