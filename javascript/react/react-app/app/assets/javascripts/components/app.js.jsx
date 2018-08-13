// Declare objects that will be used in our state
let account = {
  name: 'Fred',
  holdings: [],
  target: null 
}

let holding = {
  ticker: 'AAPL',
  price: 100.0
}

let target = {
  name: 'Balanced Mix'
}

// Set initial Global State
const initialSate = { counter: 0 }

const reducer = (state = initialSate, action) => {
  if (action.type == 'INCREMENT') {
    return {
      counter: state.counter + 1
    }
  }
  return state;
};

// get global state in the name of 'ctr'
function mapStateToProps(state) {
  return {
    ctr: state.counter
  };
};

// creates functions that can be passed to the component
// in connect
function mapDispatchToProps(dispatch) {
  return {
    onIncrementCounter: () => dispatch({type: 'INCREMENT'})
  }
}

const App = (props) => {
  const Provider = window.ReactRedux.Provider
  const store = window.Redux.createStore(reducer)

  // What we pass to connect...
  // Which part of the entire application state is interesting to us
  // What actions do I want to dispatch
  const CounterRedux = window.ReactRedux.connect(mapStateToProps, mapDispatchToProps)(Counter);

  return (
    <div className="app">
      <Provider store={store}>
        <CounterRedux />        
      </Provider>
    </div>
  )
}

class Counter extends React.Component {

  counterChangedHandler(action, value) {
    switch (action) {
      case 'inc':
      this.setState((prevState) => {
        return { counter: counter + 1 }
      });
      break;
    }
  }

  render() {
    return (
      <div>
        <h1>Counter</h1>
        <h2>{this.props.ctr}</h2>
        <button onClick={this.props.onIncrementCounter}>Add</button>
      </div>
    )
  }
}

