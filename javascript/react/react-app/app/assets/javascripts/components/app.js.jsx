const App = (props) => {
    
  const initialState = { 
    counter: 0,
    account: props.account
  }

  // ********************************
  // Reducer
  // ********************************

  // This will be passed to our store and will
  // manage state and actions
  const reducer = (state = initialState, action) => {
    console.log('REDUCER');

    switch (action.type) {
        case actionTypes.ADD_HOLDING:
            return {
                ...state,
                account: { 
                    ...state.account, 
                    holdings: state.account.holdings.concat(newHolding())
                },
                // update not triggered if *just* holding.account is updated
                counter: state.counter + 1
            }
        case actionTypes.ADD_TARGET:
            return { 
                ...state,
                account: {
                    ...state.account, 
                    target: target
                },
                counter: state.counter + 1,
            }
        case actionTypes.DELETE_HOLDING:
            return {
                ...state,
                account: { 
                    ...state.account, 
                    holdings: state.account.holdings.filter((item, index) => index !== action.index)
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

  // get global state
  function mapStateToProps(state) {
    console.log('STATE DISPATCHER');
    return {
        counter: state.counter,
        account: state.account
    };
  };

  // creates functions that can be passed to the component in connect
  function mapDispatchToProps(dispatch) {
    console.log('ACTION DISPATCHER');
    return {
        deleteHolding: (index) => dispatch({type: actionTypes.DELETE_HOLDING, index: index}),
        addHolding: () => dispatch({type: actionTypes.ADD_HOLDING}),
        addTarget: () => dispatch({type: actionTypes.ADD_TARGET})
    }
  }

  // ********************************
  // Create Redux Store
  // ********************************
  const store = window.Redux.createStore(reducer)

  // ********************************
  // Declare Components
  // ********************************

  // What we pass to connect...
  // Which part of the entire application state is interesting to us
  // What actions do I want to dispatch
  const Provider = window.ReactRedux.Provider

  // ** Must be Component in order to recieve State from Redux
  const AccountRedux = window.ReactRedux.connect(mapStateToProps, mapDispatchToProps)(Account);
  const TargetRedux = window.ReactRedux.connect(mapStateToProps, mapDispatchToProps)(Target);

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
