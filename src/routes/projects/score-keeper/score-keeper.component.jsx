import { useEffect,useState } from 'react'

import Button from '../../../components/button/button.component'

import './score-keeper.styles.scss'


const ScoreKeeper = () => { 
    
    const [score, setScore]=useState(localStorage.getItem('score')||0)

    
    useEffect(()=>{
        localStorage.setItem('score',score)
    },[score])
    
    
    return(
        
        <div className='score-keeper'>
        <h1>Twój wynik to: <span className='score'>{score}</span></h1>
        <Button buttonType='red' onClick={()=>setScore(prevScore=>parseInt(prevScore,10)+1)} >+</Button>
        <Button buttonType='red' onClick={()=>setScore(prevScore=>prevScore-1)} >-</Button>
        </div>
    )
    
}
export default ScoreKeeper