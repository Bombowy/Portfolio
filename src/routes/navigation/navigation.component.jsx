import { Outlet, Link } from "react-router-dom"
import "./navigation.styles.scss"

const Navigation = () => {
	return (
		<>
			<div className='navigation'>
			<Link className='logo-container' to='/'>
				<span className="logo">KULPOK IT</span> 
		  </Link>
				<div className='nav-links-container'>
					
					<Link className='nav-link' to='/projects'>
						PROJEKTY
					</Link>
					<Link className='nav-link' to='/games'>
						GRY
					</Link>
					
					
				</div>
			</div>
			<Outlet />
		</>
	)
}

export default Navigation
