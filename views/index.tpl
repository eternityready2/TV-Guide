<!DOCTYPE html>
<html>
	<head>
		<!-- Global site tag (gtag.js) - Google Analytics -->
		<script async src="https://www.googletagmanager.com/gtag/js?id=UA-29835449-5"></script>
		<script>
		  window.dataLayer = window.dataLayer || [];
		  function gtag(){dataLayer.push(arguments);}
		  gtag('js', new Date());

		  gtag('config', 'UA-29835449-5');
		</script>


		<title>Guide - Eternity Ready TV</title>
		<base href="/live-tv/" />
		<link href="static/css/reset.css" rel="stylesheet">
		<link href="static/css/style.css" rel="stylesheet">
		<link href="static/iframe/iframe.css" rel="stylesheet">

		<!-- <link rel="shortcut icon" href="favicon.ico" /> -->

		<meta name="description" content="Family-friendly TV guide" />
		<script src="static/js/jquery-1.11.3.js"></script>
		<script src="static/js/moment.js"></script>
		<script src="static/js/moment-timezone-with-data.js"></script>
		<script src="static/js/script.js"></script>
		<script src="static/iframe/iframe-data.js"></script>		
		<script src="static/iframe/iframe.js"></script>

		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=0">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap" rel="stylesheet">
	</head>
	<body>
		<div id="darken"></div>
		<div id="frame">

			<iframe frameborder="0" marginheight="0" marginwidth="0" src="">
			</iframe>
			<div id="frame-close">Close</div>
		</div>
		<div id="wrapper">
			<div class="move-button" id="prev"></div>
			<div class="move-button" id="next"></div>
			<div id="tv-guide">


				<ul id="days">
					<select name="select" id="timezone">
						<option value="0" selected>Pacific</option>
						<option value="-1">Mountain</option>
						<option value="-2">Central</option>
						<option value="-3">Eastern</option>
					</select>
<!-- 					<li>
						<div class="day-name">Monday</div>
						<div class="day-date">21st Sept</div>
					</li> -->
				</ul>



<!-- 				<ul id="days-concise">
					<li>M</li>
					<li>T</li>
					<li>D</li>
				</ul> -->

				<div id="channels">

					<div id="channels-container">
						<div id="current-time-bar"></div>
						<div id="time-bar">
						</div>
						<div class="channel">
							<div class="channel-logo"></div>
							<!-- <div class="channel-logo-dummy"></div> -->

							<div class="programs">
								<div class="program">
									<span class="program-desc">Test Show</span>
									<span class="program-time">9am-10am</span>
								</div>
								<div class="program">
									<span class="program-desc">Test Show</span>
									<span class="program-time">9am-10am</span>
								</div>
								<div class="program">
									<span class="program-desc">Test Show</span>
									<span class="program-time">9am-10am</span>
								</div>
							</div>

						</div>
					</div>
				</div>
			</div>

		</div>
	</body>
</html>
