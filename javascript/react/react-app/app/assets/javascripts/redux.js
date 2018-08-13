// ********************************
// State
// ********************************

// Declare objects that will be used in our state
let account = {
    name: 'Fred',
    holdings: [],
    target: null 
}

let target = {
    name: 'Balanced Mix'
}

// Set initial Global State
const initialSate = { 
    counter: 0,
    account: account
}

function randomTicker() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    for (var i = 0; i < 4; i++) text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}
function randomPrice() {
    return Math.floor(Math.random() * 1000);
}
function newHolding() {
    return {
        ticker: randomTicker(),
        price: randomPrice()
    }
}

// ********************************
// Reducer
// ********************************

// This will be passed to our store and will
// manage state and actions
const reducer = (state = initialSate, action) => {
    // clone state
    // const newState = Object.assign({}, state);


    switch (action.type) {
        case 'ADD_HOLDING':
            return {
                ...state,
                account: { 
                    ...state.account, 
                    holdings: state.account.holdings.concat(newHolding())
                },
                // update not triggered if *just* holding.account is updated
                counter: state.counter + 1
            }
        case 'ADD_TARGET':
            return { 
                ...state,
                account: {
                    ...state.account, 
                    target: target
                },
                counter: state.counter + 1,
            }
        case 'DELETE_HOLDING':
            let holdings = [...state.account.holdings];
            holdings.splice(action.index, 1);
            return {
                ...state,
                account: { 
                    ...state.account, 
                    holdings: holdings
                },
                counter: state.counter + 1,
            }
        default:
            break
    }
    return state;
};

// ********************************
// Dispatchers
// ********************************

// get global state in the name of 'ctr'
function mapStateToProps(state) {
    return {
        ctr: state.counter,
        account: state.account
    };
};

// creates functions that can be passed to the component in connect
function mapDispatchToProps(dispatch) {
    return {
        deleteHolding: (index) => dispatch({type: 'DELETE_HOLDING', index: index}),
        addHolding: () => dispatch({type: 'ADD_HOLDING'}),
        addTarget: () => dispatch({type: 'ADD_TARGET'})
    }
}

// ********************************
// Create Redux Store
// ********************************
const Provider = window.ReactRedux.Provider
const store = window.Redux.createStore(reducer)

// ********************************
// Declare Components
// ********************************

// What we pass to connect...
// Which part of the entire application state is interesting to us
// What actions do I want to dispatch

const AccountRedux = window.ReactRedux.connect(mapStateToProps, mapDispatchToProps)(Account);
const TargetRedux = window.ReactRedux.connect(mapStateToProps, mapDispatchToProps)(Target);
