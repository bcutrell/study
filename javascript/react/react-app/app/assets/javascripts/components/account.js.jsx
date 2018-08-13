
class Account extends React.Component {
    render() {
  
      const holdings = this.props.account.holdings.map((holding, index) => {
        return (
            <Holding 
                key={index}
                id={index}
                ticker={holding.ticker} 
                price={holding.price}
                deleteHolding={this.props.deleteHolding} />
        )
      })
  
      return (
        <div style={ { border: "5px solid red" } }>
          <h2>Aciton Counter: {this.props.counter}</h2>
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
  