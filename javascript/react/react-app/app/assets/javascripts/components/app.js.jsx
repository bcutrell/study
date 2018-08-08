class Row {
  constructor(id, value, type, rows) {
    this.id = id;
    this.value = value;
    this.type = type;
    this.rows = rows;
  }
}

const App = (props) => {
  return (
    <div className="app">
      <h1>App</h1>
      <Demo />
    </div>
  )
}

demoData = [
  new Row(
    0,
    'nice', 
    'lime', 
    [new Row('bad', 'lime')]
  )
]

class Demo extends React.Component {
  constructor(props) {
    super(props)
    this.state = { 
      value: '', 
      type: 'lime', 
      rows: demoData
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleDelete = this.handleDelete.bind(this);
    this.handleCreate = this.handleCreate.bind(this);
  }

  nextId() {
    return this.state.rows.length + 1;
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
    const parentId = event.target.parentId.value;
    let rows;

    if (parentId) {

      rows = this.state.rows.map( (obj) => {
        if (obj.id == parseInt(parentId)) {
          if (!obj.rows) {
            obj.rows = [];
          }
          
          obj.rows.push(new Row(this.nextId(), 'test', 'test'))
          obj.create = false;
        

        }
        return obj
      })
      
    } else {
      rows = [...this.state.rows, new Row(this.nextId(), this.state.value, this.state.type)]
    }
    
    this.setState({ 
      value: '', 
      type: 'lime',
      rows: rows
    })
    event.preventDefault();
  }

  handleCreate(index) {
    rows = this.state.rows;
    rows[index].create = true;
    this.setState({ rows: rows });
  }

  handleUpdate() {
  }

  handleDelete(index) {
    rows = this.state.rows;
    rows.splice(index, 1);

    this.setState({ rows: rows });
  }

  render() {
    return (
      <div>
        <Form 
          handleSubmit={this.handleSubmit} 
          handleChange={this.handleChange} 
          value={this.state.value} 
          type={this.state.type} />

        < List 
          items={this.state.rows} 
          handleSubmit={this.handleSubmit}
          handleCreate={this.handleCreate}
          handleDelete={this.handleDelete} 
        />
      </div>
    )
  }
}

const Form = (props) => {
  return (
    <form onSubmit={props.handleSubmit}>
      <label>
        Name:
        <input type="text" value={props.value} name="value" onChange={props.handleChange} />
        <input type="hidden" value={props.parentId} name="parentId"/>

          <select value={props.type} name="type" onChange={props.handleChange}>
            <option value="grapefruit">grapefruit</option>
            <option value="lime">lime</option>
          </select>
      </label>
      <input type="submit" value="Submit" />
    </form>
  )
}

// https://stackoverflow.com/questions/37387351/reactjs-warning-setstate-cannot-update-during-an-existing-state-transiti
const List = (props) => {
  let subList,
      createForm;

  const listItems = props.items.map((item, index) => {
    let subList;
    if (item.rows && item.rows.length > 0) {
      subList = < List items={item.rows} handleDelete={props.handleDelete} />
    }

    if (item.create) {
      createForm = <Form 
      handleSubmit={props.handleSubmit} 
      parentId={item.id} 
      />
    }

    const display = (
    <li key={index}>
      value: {item.value} type: {item.type}
      <button onClick={() => props.handleCreate(index)}>Create</button>
      <button onClick={() => props.handleUpdate}>Update</button>
      <button onClick={() => props.handleDelete(index)}>Delete</button>
      { createForm }
      { subList }
    </li>
    )

    return display
  })

  return (
  <ul>
    { listItems }
  </ul>)
};
