import { Link } from "react-router-dom"

import "./projects.styles.scss"

const Projects = () => {
	return (
		<div className="body-projects">
			<span className='title-projects'> Moje Projekty</span>
			
			<Link className="project-link" to='color-renderer'>Color Renderer</Link>
			
			<Link className="project-link"  to='dark-mode'>Dark Mode</Link>
			
			<Link className="project-link"  to='form-validator'>Form Validator</Link>
			<Link className="project-link"  to='dog-pictures'>Dog pictures</Link>
			<Link className="project-link"  to='score-keeper'>Score keeper</Link>
			<Link className="project-link"  to='pixel-art'>Pixel Art</Link>
			<Link className="project-link"  to='simple-calculator'>Simple calculator</Link>
			<Link className="project-link"  to='shopping-cart'>Shopping Cart</Link>
		</div>
	)
}
export default Projects
