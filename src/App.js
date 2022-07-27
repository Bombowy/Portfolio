import { Routes, Route } from "react-router-dom"

import Navigation from "./routes/navigation/navigation.component"
import Home from "./routes/home/home.component"

import Projects from "./routes/projects/projects.component"

import ColorRenderer from "./routes/projects/color-renderer/color-renderer.component"
import DarkMode from "./routes/projects/dark-mode/dark-mode.component"
import FormValidator from "./routes/projects/form-validator/form-validator.component"
import DogPictures from "./routes/projects/dog-pictures/dog-pictures.component"
import ScoreKeeper from "./routes/projects/score-keeper/score-keeper.component"
import PixelArt from "./routes/projects/pixel-art/pixel-art.component"
import SimpleCalculator from "./routes/projects/simple-calculator/simple-calculator.component"
import ShoppingCart from "./routes/projects/shopping-cart/shopping-cart.component"

const App = () => {
	return (
		<Routes>
			<Route path='/' element={<Navigation />}>
				<Route index element={<Home />} />
				<Route path='projects' element={<Projects />} />
				<Route path='projects/color-renderer' element={<ColorRenderer />} />
				<Route path='projects/dark-mode' element={<DarkMode />} />
				<Route path='projects/form-validator' element={<FormValidator />} />
				<Route path='projects/dog-pictures' element={<DogPictures />} />
				<Route path='projects/score-keeper' element={<ScoreKeeper />} />
				<Route path='projects/pixel-art' element={<PixelArt />} />
				<Route path='projects/pixel-art' element={<PixelArt />} />
				<Route
					path='projects/simple-calculator'
					element={<SimpleCalculator />}
				/>
				<Route path='projects/shopping-cart' element={<ShoppingCart />} />
			</Route>
      </Routes>
		
	)
}

export default App
