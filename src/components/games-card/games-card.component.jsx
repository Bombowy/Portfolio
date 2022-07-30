import './games-card..styles.scss'
import '../../routes/games/games.styles.scss'

const GameCard = ({name,img,link}) => {
    return(
        <div className='game-card-container'>
        <img className='game-image'src={img} alt="memories game image" />
            <div className="game-card-footer">
                <span className="game-card-footer-name">{name}</span>
                <a className='' href={link}><button className='game-link-button'>ZAGRAJ</button></a>       
    
            </div>
        </div>
    )
}
export default GameCard