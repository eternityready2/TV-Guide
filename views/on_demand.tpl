<!DOCTYPE html>
<html>

    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-29835449-5"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag () { dataLayer.push( arguments ); }
            gtag( 'js', new Date() );

            gtag( 'config', 'UA-29835449-5' );
        </script>
        <title>On Demand - Eternity Ready TV</title>
        <base href="/live-tv/on-demand" />
        <link href="static/css/reset.css" rel="stylesheet">
        <link href="static/iframe/iframe.css" rel="stylesheet">
        <link href="static/css/on-demand-style.css" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap" rel="stylesheet">

        <meta name="description" content="On Demand TV" />

        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=0">

        <script>
            window.onDemandChannelTitles = [
                % for title in channel_titles:
                    "{{ title }}",
                % end
            ]


        </script>
    </head>

    <body>
        <div class="overlay"></div>
        <header>
            <div class="sidebar-toggle">☰</div>
            <div class="logo"><img src="/live-tv/static/iframe/logo-s.png" alt="logo"></div>

            <div>
                <div class="search-container">
                    <input type="search" placeholder="Find a channel" />
                    <ul class="search-results">
                    </ul>
                </div>
            </div>


            <div class="links"><a href="/live-tv" class="top-link">Live TV</a><a
                    href="https://eternityready.tv/on-demand#" class="top-link-active">On Demand</a></div>
        </header>
        <aside>
            <ul>
                
                <li>
                    <h4>WATCH NOW</h4>
                </li>
                <li><a href="/live-tv/">Live TV</a></li>
                <li><a href="https://eternityready.tv/on-demand#">On Demand</a></li>
                <li>
                    <h4>MORE ABOUT ETERNITY READY TV</h4>
                </li>
                <li><a href="http://www.eternityreadyradio.com" target="_blank">Music & Podcasts</a></li>
                <li><a href="http://www.raptureready.tv" target="_blank">Rapture Ready TV</a></li>
                <li><a href="https://help.eternityready.com" target="_blank">Contact Us</a></li>
                <li><a href="https://donorbox.org/eternity-ready-radio" target="_blank">Donate</a></li>
                <li style="padding-top: 20px;">
                    <h4 class="mb">MOBILE APPS</h4>
                </li>
                <li style="margin-top: 20px;"><a
                        href="https://play.google.com/store/apps/details?id=com.wEternityReadyRadio&amp;hl=en_US&amp;gl=US"
                        class="mb" target="_blank"><img src="/live-tv/static/iframe/google-s.svg" alt="Play Store"></a>
                </li>
                <li style="margin-top: 20px;"><a href="https://apps.apple.com/us/app/eternity-ready/id1564486246"
                        class="mb" target="_blank"><img alt="apple store" src="/live-tv/static/iframe/apple-s.svg"></a>
                </li><small>@2023
                    Eternity Ready. All rights reserved.</small>
            </ul>
        </aside>




        <div id="darken"></div>
        <div class="live-iframe open">
            <!-- <div onclick="closeIframe()" class="close-btn"></div> -->
            <div class="live-iframe-wrap">
                <iframe 
                    width="560" 
                    height="315"
                    src=""
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen
                ></iframe>
            </div>
        </div>

        <div id="wrapper">

            <div class="categories-toggle" onclick="toggleCategories()">Categories</div>
            

            <div class="categories">
                <ul>
                    % for category in categories:
                        <li onclick='onCategoryClick("{{ category }}")'>{{ category }}</li>
                    % end
                </ul>
            </div>
          
            
            <div class="category-grids">
                % for category in categories:
                    <div data-category="{{category}}" class="category-grid-container">
                        <h2 class="category-title" data-category="{{category}}">{{category}}</h2>
                        <div class="channels-slider">
                            <div tabindex="-1" class="arrow arrow-left" onclick="slideLeft(event)"><</div>
                            <div tabindex="-1" class="arrow arrow-right" onclick="slideRight(event)">></div>
                            <div class="channels">
                                % for title in categories[category]:
                                    <div data-channel="{{categories[category][title]['title']}}" tabindex="0" onclick='onListItemClick("{{categories[category][title]['title']}}")' class="channel">
                                        <h3>{{categories[category][title]['title']}}</h3>
                                        <p>{{categories[category][title]['description']}}</p>
                                        <img src="/live-tv/static/img/on_demand/{{categories[category][title]['image']}}" />
                                        <div class="channel-overlay"></div>
                                        <div class="iframe-code">
                                            {{categories[category][title]["iframe"]}}
                                        </div>
                                    </div>
                                % end
                            </div>

                        </div>
                    </div>
                % end
            </div>
            
        </div>
        <script src="static/iframe/on-demand-script.js"></script>

    </body>

</html>
