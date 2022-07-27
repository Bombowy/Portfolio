import { useState } from "react"
import "./shopping-cart.styles.scss"



const items = [
	{
		name: "Jabłko",
		price: "0.61",
	},
	{
		name: "Gruszka",
		price: "0.82",
	},
	{
		name: "Banan",
		price: "0.93",
	},
]

const ShoppingCart = () => {
	const [cart, setCart] = useState([])

	const addToCart = (item) => {
		const cartCopy = [...cart]
		const itemInCart = cartCopy.find((i) => item.name === i.name)
		if (itemInCart) {
			itemInCart.quantity += 1
			setCart(cartCopy)
		} else {
			setCart((prevCart) => [...prevCart, { ...item, quantity: 1 }])
		}
	}
	const increase = (name) => {
		const cartCopy = [...cart]
		const item = cartCopy.find((i) => i.name === name)
		item.quantity += 1
		setCart(cartCopy)
	}
	const decrease = (name) => {
		let cartCopy = [...cart]
		const item = cartCopy.find((i) => i.name === name)
		if (item.quantity > 1) {
			item.quantity -= 1
		} else {
			cartCopy = cartCopy.filter((i) => i.name !== name)
		}

		setCart(cartCopy)
	}


	return (
		<div className="shopping">
			<h1>Koszyk sklepowy</h1>
			<div className='shopping-cart'>
				<div className='items'>
					<h2>Produkty</h2>
                    <br />
					{items.map((item) => (
						<div key={item.name}><br />
							<h3>{item.name}</h3><br />
							<p>{item.price}</p><br />
							<button onClick={() => addToCart(item)}>Dodaj do koszyka</button>
						</div>
					))}
				</div>
				<div>
					<h2>Koszyk</h2><br />
					{cart.map((item) => (
						<div key={item.name}><br />
							<h3>{item.name}</h3><br />
							<p>
								<button className="shopping-cart-btn" onClick={() => decrease(item.name)}>-</button>
								{item.quantity}
								<button className="shopping-cart-btn"  onClick={() => increase(item.name)}>+</button>
							</p>
							<p>Subtotal: ${(item.quantity * item.price).toFixed(2)}</p>
						</div>
					))}
				</div>
			</div>
			<div className='total'>
            <h2>
            Łącznie: ${cart.reduce((acc,i)=>acc+(i.quantity*i.price),0).toFixed(2)}
        </h2>
			</div>
		</div>
	)
}
export default ShoppingCart
