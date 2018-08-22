import React, { Component } from 'react';
import { connect } from 'react-redux';

import CheckoutSummary from '../../components/Order/CheckoutSummary/CheckoutSummary';
import ContactData from './ContactData/ContactData';

import { Route, Redirect } from 'react-router-dom';
import * as actions from '../../store/actions/index';


class Checkout extends Component {

    componentWillMount() {
        this.props.onInitPurchase();
    }

    onCheckoutContinued = () => {
        this.props.history.replace('/checkout/contact-data');
    }

    onCheckoutCancelled = () => {
        this.props.history.goBack();
    }

    render() {
        let summary = <Redirect to="/" />

        if (this.props.ings) {
            const purchasedRedirect =this.props.purchased ? <Redirect to="/" /> : null
            summary = (
                <div>
                    { purchasedRedirect }
                    <CheckoutSummary
                    onCheckoutCancelled={this.onCheckoutCancelled}
                    onCheckoutContinued={this.onCheckoutContinued}
                    ingredients={this.props.ings} />
                    <Route path={this.props.match.url + "/contact-data"}
                        component={ContactData}/>
                </div>
            )
        }

        return summary
    }
}


const mapStateToProps = state => {
    return {
        ings: state.burgerBuilder.ingredients,
        purchased: state.order.purchased
    };
}

const mapDispatchToProps = dispatch => {
    return {
        onInitPurchase: () => dispatch(actions.purchaseInit())
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(Checkout);
