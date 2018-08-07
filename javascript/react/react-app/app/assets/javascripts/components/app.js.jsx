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
    this.state = { value: '', type: 'lime'};

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
        < Rows />
      </div>
    )
  }
}

const Rows = (props) => {
  return (
      <ul>
        <li>Rows 1</li>
      </ul>
  )
}
