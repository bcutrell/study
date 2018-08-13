class Target extends React.Component {

    generateAllocation() {
      let text = "";
      const nHoldings = this.props.account.holdings.length
      if (nHoldings > 0) {
        let weight = 100;
        
        text = this.props.account.holdings.map((holding, index) => {
          return (
            <li key={index}> {holding.ticker} {weight / nHoldings} </li>
          )
        })
      }
      return text;
    }
  
    render() {
      allocation = this.generateAllocation();
  
      return (
        <div style={ { border: "3px solid blue" } }>
          <h2>Target Allocation</h2>
          <ul> {allocation} </ul>
        </div>
      )
    }
  }