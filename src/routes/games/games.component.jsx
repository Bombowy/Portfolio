import GameCard from "../../components/games-card/games-card.component"

import "./games.styles.scss"

const Games = () => {
	return (
		<div className='games'>
			<div className='games-container'>
				<GameCard
					name='Memories'
					img={require("../../assets/memories.jpg")}
					link='https://bombowy.github.io/memories/'></GameCard>
				<GameCard
					name='Wisielec'
					img={require("../../assets/wisielec.jpg")}
					link='https://bombowy.github.io/wisielec/'></GameCard>
			</div>
		</div>
	)
}

export default Games
