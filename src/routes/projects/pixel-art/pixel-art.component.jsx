import React, { createContext, useContext, useState } from "react"

import "./pixel-art.styles.scss"
import "../projects.styles.scss"

const ColorContext = createContext({
	color: "lightGrey",
	setColor: () => {},
})

const ColorPicker = () => {
	const colors = ["red", "blue", "yellow", "green", "black", "white", "purple"]
	const { setColor } = useContext(ColorContext)

	return (
		<div>
			<h1>Wybierz kolor</h1>
			{colors.map((color) => (
				<button
					className='pixel'
					onClick={() => setColor(color)}
					key={color}
					style={{ backgroundColor: color }}
				/>
			))}
		</div>
	)
}
const Pixel = () => {
	const { color } = useContext(ColorContext)
	const [pixelColor, setPixelColor] = useState("lightGrey")

	return (
		<div
			onClick={() => setPixelColor(color)}
			style={{
				height: "20px",
				width: "20px",
				margin: "1px",
				backgroundColor: pixelColor,
			}}
		/>
	)
}

const Pixels = () => {
	const pixels = []
	for (let i = 0; i < 100; i++) pixels.push(<Pixel />)
	return <div className='tab'>{pixels}</div>
}

const PixelArt = () => {
	const [color, setColor] = useState("lightGrey")

	return (
		<ColorContext.Provider value={{ color, setColor }}>
			<div className='pixelart'>
				<ColorPicker />
				<Pixels />
			</div>
		</ColorContext.Provider>
	)
}
export default PixelArt
