import React, { Component } from 'react';
// import classes from './OrderSummary.css';

import Button from '../../UI/Button/Button';
import Aux from '../../../hoc/Aux';

class OrderSummary extends Component {
    // this could be a functional component

    render() {
        const ingredientSummary = Object.keys(this.props.ingredients)
            .map(igKey => {
                return <li key={igKey}><span style={{ textTransform: 'capitalize' }}>{igKey}</span>: {this.props.ingredients[igKey]}</li>
            });

        return (
            <Aux>
                <h3>Your Order</h3>
                <ul>
                    { ingredientSummary }
                </ul>
                <p><strong>Total Price: {this.props.price.toFixed(2)}</strong></p>
                <Button btnType="Danger" clicked={this.props.purchaseCanceled}>CANCEL</Button>
                <Button btnType="Success" clicked={this.props.purchaseContinue}>CONTINUE</Button>
            </Aux>
        );
    }    
}

export default OrderSummary;
