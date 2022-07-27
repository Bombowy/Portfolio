import { useState } from "react"

import './form-validator.styles.scss'


const FormValidator = () => { 
    const [email,setEmail]=useState('')
    const [password,setPassword]=useState('')
    const [passwordConfirm,setPasswordConfirm]=useState('')

    const [message,setMessage]=useState('')
    const findErrors=()=>{
        const errors=[]
        if(!email||!password||!passwordConfirm)errors.push('Wszystkie pola muszą być uzupełnione')
        if([...email].filter(i=>i==='@').length !==1){
            errors.push('Email musi posiadać @')
        }
        if(password.length<8)errors.push('Hasło musi być dłuższe niż 8 znaków')
        if(password!==passwordConfirm) errors.push('Hasła się nie zgadzają')
        return errors

    }
    const handleSubmit = e =>{
        e.preventDefault()

        const errors=findErrors()
        setMessage(errors.length?errors.join(', '):'Utworzono użytkownika')
    }
   
    return(
        <div className="form-validator">
<form onSubmit={handleSubmit}>
<h2>Zarejestruj się</h2>
<label htmlFor="email">Email</label>
<input type="text"name="email"onChange={e=>setEmail(e.target.value)} />
<br />
<label htmlFor="password">Hasło</label>
<input type="password" name="password" onChange={e=>setPassword(e.target.value)} />
<br />
<label htmlFor="password-confirm">Potwierdź hasło</label>
<input type="password" name="password-confirm" onChange={e=>setPasswordConfirm(e.target.value)} />
<br />
{message}
<br />
<input type="submit" value='Submit'  />
</form>

        </div>
    )
 }
 export default FormValidator