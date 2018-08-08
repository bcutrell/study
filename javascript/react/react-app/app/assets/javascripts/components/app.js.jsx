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
    this.handleDelete = this.handleDelete.bind(this);
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
    console.log(this.state);
    this.setState({ 
      value: '', 
      type: 'lime', 
      rows: [...this.state.rows, { value: this.state.value, type: this.state.type }]
    })
    event.preventDefault();
  }

  handleDelete(index) {
    rows = this.state.rows;
    rows.splice(index, 1);

    this.setState({
      rows: rows
    });
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
        < List items={this.state.rows} handleDelete={this.handleDelete} />
      </div>
    )
  }
}

const List = (props) => (
  <ul>
    {
      props.items.map((item, index) => 
        <li key={index}>
          Value: {item.value} Type: {item.type}
          <button onClick={() => props.handleDelete(index)}>Delete</button>
        </li>
      )
    }
  </ul>
);
