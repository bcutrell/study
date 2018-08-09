// Redux - because state management can be hard

// Central Store - Stores entire applicaiton state

// Action: pre-defined information package (possibly with payload)
// Reducer: Recieve action and update state (pure sync functions, no side-effects)
//
// Component -> Dispatches -> Action -> Reducers -> 
//   Central Store -> Subscription -> 
// Component
//
// Central Store triggers Subscription which updates the component state

const redux = require('redux');
const createStore = redux.createStore;

const initialState = {
  counter: 0
}

// Reducer
const rootReducer = (state = initialState, action) => {

  // NEVER MUTUATE STATE
  if (action.type == 'INC_COUNTER') {
    return {
      ...state,
      counter: state.counter + 1
    }
  }

  if (action.type == 'ADD_COUNTER') {
    return {
      ...state,
      counter: state.counter + action.value
    }
  }
  return state;
}

// Store
// store needs reducer
const store = createStore(rootReducer);
console.log(store.getState());

// Subscription
// to avoid always using getState
// triggered whenever the state is updated
store.subscribe(() => {
  console.log('[Subscription]', store.getState());
});

// Dispatching Action
// Action is the argument to store.dispatch
store.dispatch({type: 'INC_COUNTER'});
console.log('Dispatch INC_COUNTER');
console.log(store.getState());
store.dispatch({type: 'ADD_COUNTER', value: 10});
console.log('Dispatch ADD_COUNTER');
console.log(store.getState());

