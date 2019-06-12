// React updates when state or prop changes

// Use stateless components as much as possible
// only containers should change state
const Person = (props) => {
  return (
      <div>
        <p onClick={props.click} > My name is { props.name } </p>
        <p> { props.children } </p>

        <input type="text" 
          onChange={props.changed} 

          // IF using a value prop
          // an onChange function is required!!!
          //
          // adding value creates two way binding
          value={props.name}
        />
      </div>
  )
}

// state -> managed inside component
// changing state will cause component to rerender
//
// props -> passed into components
class App extends Component {
  state = {
    persons: [
      { name: 'Max' },
      { name: 'Manu' }
    ]
  }

  // By using ES6 syntax
  // we can continue to use the class 'this' keyword
  switchNameHandle = (newName) => {
    // DON'T DO THIS
    // this.state.persons[0].name = 'Maximillion'

    // if state is not referenced in setState
    // it will not be changed
    this.setState({
      persons: [
        { name: newName } 
      ]
    })
  }

  nameChangedHandler = (event) => {
    this.setState({
      persons: [
        { name: event.target.value } 
      ]
    })
  }


  // this refers to class
  render() {
    return (
        <div className="app">
          <button onClick={this.switchNameHandle}> Swtich Name </button>
          <Person 
            changed={this.nameChangeHandler}

            // The best way to best function is to use bind this
            click={this.swithcNameHandle.bind(this, 'Maximilian')} 
            name={this.state.persons[0].name}>
            I have many hobbies
          </Person>

          <Person 

            // This is the alternative that is more likely to cause performance issues
            // passing annon function that will get executed on click
            click={() => this.swithcNameHandle('Maximilian!!')} 
            name={this.state.persons[0].name}>
            I have many hobbies
          </Person>

        </div>
  }
}


