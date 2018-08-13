const App = (props) => {
  return (
    <div className="app">
      <Provider store={store}>
        <div>
          <AccountRedux />
          <TargetRedux />
        </div>
      </Provider>
    </div>
  )
}

class Account extends React.Component {
  render() {

    const holdings = this.props.account.holdings.map((holding, index) => {
      return (
        <li key={index}> 
          
          Ticker: { holding.ticker } Price: { holding.price }
          <button onClick={this.props.deleteHolding.bind(this, index)}>Delete</button>
        </li>
      )
    })

    return (
      <div>
        <h2>Aciton Counter: {this.props.ctr}</h2>
        <p>{this.props.account.name}</p>
        <button onClick={this.props.addHolding}>Add Holding</button>
        <button onClick={this.props.addTarget}>Add Target</button>
        <p> Target: {this.props.account.target ? this.props.account.target.name : 'No Target'}</p>
        <ul> { holdings } </ul>
      </div>
    )
  }
}

// **Must be Component in order to recieve State from Redux
class Target extends React.Component {

  genAllocation() {

  }

  render() {

    return (
      <h2>Target Allocation</h2>
    )
  }
}

const Holding = (props) => {
  // return ()
}