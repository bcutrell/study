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
    this.state = { 
      value: '', 
      type: 'lime', 
      rows: []
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleDelete = this.handleDelete.bind(this);
  }

  handleChange(event) {
    const target = event.target;
    
    const value = target.value;
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
               <option value="grapefruit">grapefruit</option>
               <option value="lime">lime</option>
             </select>
          </label>
          <input type="submit" value="Submit" />
        </form>
        < List items={this.state.rows} handleDelete={this.handleDelete} />
      </div>
    )
  }
}


// https://stackoverflow.com/questions/37387351/reactjs-warning-setstate-cannot-update-during-an-existing-state-transiti
const List = (props) => (
  <ul>
    {
      props.items.map((item, index) => 
        <li key={index}>
          value: {item.value} type: {item.type}
          <button onClick={() => props.handleDelete(index)}>Create</button>
          <button onClick={() => props.handleDelete(index)}>Update</button>
          <button onClick={() => props.handleDelete(index)}>Delete</button>
        </li>
      )
    }
  </ul>
);

// const ListItem = (props) => (
// )

// const UpdateListItem = (props) => (
// )