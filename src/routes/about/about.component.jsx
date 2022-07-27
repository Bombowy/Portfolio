import "./about.styles.scss"

const About = () => {
	return (
		<>
			<div className='about-me-section aboutme-inside my-5'>
				<div className='d-flex flex-column'>
					<span className='about-me-text'>O mnie</span>
					<span className='why-text-sub'>Dlaczego Ja?</span>
					<div className='row justify-content-center shadow-lg my-5'>
						<div className='col-lg-6 col-md-6 col-sm-12 d-flex align-items-center justify-content-center'>
							<lottie-player
								src='https://assets3.lottiefiles.com/packages/lf20_v1yudlrx.json'
								background='transparent'
								speed='1'
								style={{ width: "500px", height: "500px" }}
								loop
								autoplay></lottie-player>
						</div>

						<div className='col-lg-6 col-md-6 col-sm-12 py-5 d-flex flex-column'>
							<span className='some-text-about-me'>
								Nazywam się Patryk Kulpok jestem studentem informatyki o
								specjalizacji programowanie uczęszczającym do Wyższej Szkoły
								Bankowej. Specjalizuje się frontendem w React, a w niedalekiej
								przyszłości chcę zostać fullstack developerem.
							</span>
							<span className='few-highlights'>
								<span className='few-text'>
									Moje najważniejsze umiejętności to:{" "}
								</span>
								<span className='few-list'>
									<ul>
										<li>HTML5</li>
										<li>CSS3/SCSS</li>
										<li>JavaScript</li>
										<li>React.js</li>
										<li>SQL</li>
										<li>Bootstrap</li>
									</ul>
								</span>
							</span>
						</div>
					</div>
				</div>
			</div>
		</>
	)
}
export default About
// <span>
// 							Nazywam się Patryk Kulpok jestem studentem informatyki o
// 							specjalizacji programowanie uczęszczającym do Wyższej Szkoły
// 							Bankowej. Moje najważniejsze umiejętności to :
// 							<ul>
// <li>HTML5</li>
// 								<li>CSS3/SCSS</li>
// 								<li>JavaScript</li>
// 								<li>React.js</li>
// 								<li>Bootstrap</li>
// 							</ul>
// 						</span>
// <lottie-player
// 	src='https://assets3.lottiefiles.com/packages/lf20_v1yudlrx.json'
// 	background='transparent'
// 	speed='1'
// 	style={{ width: "500px", height: "500px" }}
// 	loop
// 	autoplay></lottie-player>
