import { useReducer } from "react"
import "./simple-calculator.styles.scss"


const initialState = {
	num1: 0,
	num2: 0,
	result: "Brak wyniku",
}

const reducer = (state, action) => {
	if (action.type === "SET_NUM_ONE") return { ...state, num1: action.number }
	if (action.type === "SET_NUM_TWO") return { ...state, num2: action.number }
	if (action.type === "ADD")
		return { ...state, result: state.num1 + state.num2 }
	if (action.type === "SUBSTRACT")
		return { ...state, result: state.num1 - state.num2 }
	if (action.type === "CLEAR") return initialState
}

const SimpleCalculator = () => {
	const [state, dispatch] = useReducer(reducer, initialState)

	const numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	return (
		<div className='calc'>
			<div>
				<div>
					<h2>Liczba 1</h2>
					{numbers.map((number) => (
						<button
							className='calc-btn'
							key={number}
							onClick={() => dispatch({ type: "SET_NUM_ONE", number })}>
							{number}
						</button>
					))}
				</div>
                
				<div>Liczba 2</div>
				{numbers.map((number) => (
					<button
						className='calc-btn'
						key={number}
						onClick={() => dispatch({ type: "SET_NUM_TWO", number })}>
						{number}
					</button>
				))}
			</div>
			<div>
				<h2>Akcje</h2>
				<button className='calc-btn' onClick={() => dispatch({ type: "ADD" })}>
					+
				</button>
				<button
					className='calc-btn'
					onClick={() => dispatch({ type: "SUBSTRACT" })}>
					-
				</button>
				
			</div>
			<div>
				<h2>Wynik: {state.result}</h2>
                <button
					className='calc-btn-clear'
					onClick={() => dispatch({ type: "CLEAR" })}>
					Wyczyść
				</button>
			</div>

		</div>
	)
}
export default SimpleCalculator
