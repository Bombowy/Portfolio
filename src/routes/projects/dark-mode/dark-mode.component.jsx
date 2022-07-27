import { useState } from "react"
import Button from "../../../components/button/button.component"
import "./dark-mode.styles.scss"


const DarkMode = () => {
	const [darkMode, setDarkMode] = useState(false)

	return (
		<div className={` bgc ${darkMode ? "dark-mode" : ""}`}>
			<Button buttonType='transparent' onClick={() => setDarkMode(true)}>
				Dark Mode
			</Button>
			<Button buttonType='red' onClick={() => setDarkMode(false)}>
				Light Mode
			</Button>
		</div>
	)
}
export default DarkMode
