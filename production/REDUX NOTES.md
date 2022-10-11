REDUX NOTES
store-takes a reducer
-has a method called getState() which returns the current state
-has a method called dispatch() which is used to update the store
-dispatch takes an action object
Actions - object with a type(name of the action) and any additional field is known as a payload
Action creator - creates and returns an action object
Reducer - function takes an action and initial state has a switch loop 
which decides whether to update or not the state and returns a new state