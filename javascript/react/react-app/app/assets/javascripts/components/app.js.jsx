const App = (props) => {
  return (
    <div className="app">
      <h1>App</h1>
      <Demo />
    </div>
  )
}

class Demo extends React.Component {
  constructor(props) {
    super(props)
    this.state = { value: '', type: 'lime', rows: []};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    const target = event.target;
    const value = target.value; // target.type === 'select' ? target.checked : target.value;
    const name = target.name;

    this.setState({
      [name]: value
    });
  }

  handleSubmit(event) {
    // alert('A name was submitted: ' + this.state );
    console.log(this.state);
    this.state.rows.push({ value: this.state.value, type: this.state.type})
    this.setState({ value: '', type: 'lime', rows: this.state.rows })
    event.preventDefault();
  }

  render() {
    return (
      <div>
        <form onSubmit={this.handleSubmit}>
          <label>
            Name:
            <input type="text" value={this.state.value} name="value" onChange={this.handleChange} />

             <select value={this.state.type} name="type" onChange={this.handleChange}>
               <option value="grapefruit">Grapefruit</option>
               <option value="lime">Lime</option>
             </select>

          </label>
          <input type="submit" value="Submit" />
        </form>
        < Rows data={this.state.rows} />
      </div>
    )
  }
}

const Rows = (props) => {
  var items = props.data.map((row, index) => 
    <li key={index} >
      Value: {row.value} Type: {row.type}
      <button>Delete</button>
    </li>
  )
  return (
      <ul>
        { items }
      </ul>
  )
}
