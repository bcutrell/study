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
        <p>Account Name: {this.props.account.name}</p>
        <button onClick={this.props.addHolding}>Add Holding</button>
        <button onClick={this.props.addTarget}>Add Target</button>
        <p> Target: {this.props.account.target ? this.props.account.target.name : 'No Target'}</p>
        <h2> Holdings </h2>
        <ul> { holdings } </ul>
      </div>
    )
  }
}

// ** Must be Component in order to recieve State from Redux
class Target extends React.Component {

  genAllocation() {
    text = ""
    const nHoldings = this.props.account.holdings.length
    if (nHoldings > 0) {
      let weight = 100;
      
      text = this.props.account.holdings.map((holding, index) => {
        return (
          <li> {holding.ticker} {weight / nHoldings} </li>
        )
      })
    }
    return text;
  }

  render() {
    allocation = this.genAllocation();

    return (
      <div>
        <h2>Target Allocation</h2>
        <ul> {allocation} </ul>
      </div>
    )
  }
}

const Holding = (props) => {
  // return ()
}