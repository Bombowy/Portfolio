import { Link } from "react-router-dom"

import About from "../about/about.component"

import Button from "../../components/button/button.component"

import "./home.styles.scss"
const Home = () => {
	const myImg = require("../../assets/home-section-img.jpg")

	

	return (
		<>
			<div className='home'>
				<div className='home-section'>
					<div className='home-section-text'>
						<span>
							{" "}
							Witaj, jestem{" "}
							<span className='home-section-text-name'>Patryk Kulpok</span>
						</span>
						<span className='home-section-text-enthusiastic'>Entuzjaztyczny Dev 😎</span>
						<span className='home-section-text-subheading'>
							Z talentem do pisania aplikacji
						</span>
						<div className='buttons-container'>
						<a href="https://www.linkedin.com/in/patryk-kulpok-2928a421a/"><Button buttonType='transparent'>To Ja</Button></a>	
						
							<Link to='/projects'>
								<Button buttonType='red'>Moje Projekty</Button>
							</Link>
						</div>
					</div>
					<div className='home-section-image'>
						<div className='myImage'>
							<img src={myImg} alt='Patryk Kulpok programista react' />
						</div>
					</div>
				</div>
			</div>

			<About/>
		</>
	)
}

export default Home
