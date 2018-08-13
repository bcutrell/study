
const Holding = (props) => {
    return (
        <li style={ { border: "1px solid green" } }> 
            Ticker: { props.ticker } Price: { props.price }
            <button onClick={props.deleteHolding.bind(this, props.id)}>Delete</button>
        </li>
    )
}
