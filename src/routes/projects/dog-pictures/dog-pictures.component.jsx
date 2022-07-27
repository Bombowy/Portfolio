import { useEffect,useState } from 'react'

import Button from '../../../components/button/button.component'

import './dog-pictures.styles.scss'



const DogPictures = () => {
const API='https://dog.ceo/api/breeds/image/random'

const getDogPic=async()=>{
    const response = await fetch(API)
    const dog = await response.json()
    return dog.message
}

const [dogPic,setDogPic]=useState('')

useEffect(()=>{
    getDogPic().then(pic=>setDogPic(pic))
},[])

const changeDog=async()=>{
    setDogPic(await getDogPic())
}
    return(
        <div className='dog-pics'>
        <Button buttonType='transparent' onClick={changeDog}>Losuj psa</Button>
        <br />
        <br />
            <img className='dog' src={dogPic} alt="zdjęcie losowego psa" />
        </div>
    )
}
export default DogPictures