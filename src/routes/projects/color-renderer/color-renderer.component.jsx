import Color from "./color.component"
import './color-renderer.styles.scss'
const colors = [
	{
		hex: "#91A6FF",
		name: "Cornflower Blue",
	},
	{
		hex: "#FF88DC",
		name: "Persian Pink",
	},
	{
		hex: "#90FF72",
		name: "Screamin Green",
	},
	{
		hex: "#Fb4d46",
		name: "Tart Orange",
	},
]

const ColorRenderer = () => {
	return (
		<div className='body-color'>
			<div>
				{colors.map((color) => (
					<Color key={color.hex} hex={color.hex} name={color.name} />
				))}
			</div>
		</div>
	)
}

export default ColorRenderer
