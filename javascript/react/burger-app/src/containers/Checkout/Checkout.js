import React, { Component } from 'react';
import { connect } from 'react-redux';

import CheckoutSummary from '../../components/Order/CheckoutSummary/CheckoutSummary';
import ContactData from './ContactData/ContactData';

import { Route } from 'react-router-dom'

class Checkout extends Component {

    onCheckoutContinued = () => {
        this.props.history.replace('/checkout/contact-data');
    }

    onCheckoutCancelled = () => {
        this.props.history.goBack();
    }
    
    render() {
        return (
            <div>
                <CheckoutSummary 
                    onCheckoutCancelled={this.onCheckoutCancelled}
                    onCheckoutContinued={this.onCheckoutContinued}
                    ingredients={this.props.ings} />
                <Route path={this.props.match.url + "/contact-data"} 
                    component={ContactData}/>
            </div>
        )}
}


const mapStateToProps = state => {
    return {
        ings: state.ingredients
    };
}

export default connect(mapStateToProps)(Checkout);
