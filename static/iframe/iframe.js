// Extra links
const extraItems = {
    "On-Demand": "https://eternityready.tv/on-demand",
    // "Live Radio": "https://www.eternityreadyradio.com/player",
    // "Rapture Ready TV": "https://www.raptureready.tv",
    // "Contact us": "https://help.eternityready.com",
    // "Donate": "https://donorbox.org/eternity-ready-radio",
}
function loadGoogleAnalytics(){
    var ga = document.createElement('script'); 
    ga.type = 'text/javascript'; 
    ga.async = true;
    ga.src = 'https://www.googletagmanager.com/gtag/js?id=UA-29835449-5';

    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(ga, s);
}



loadGoogleAnalytics();
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'UA-29835449-5');

function initIframe(){
    if (!window.iframeData) {
        console.error("No iframe data found")
        return
    }

    // New sidebar menu
    const menuContainerEl = document.createElement("div")
    document.body.insertBefore(menuContainerEl, document.body.firstChild)
    menuContainerEl.classList.add("menu-container")
    
    // Toggle bar
    const toggleEl = document.createElement("div")
    document.body.insertBefore(toggleEl, document.body.firstChild)
    toggleEl.classList.add("nav-toggle")
    toggleEl.innerHTML = "Select category <strong>All</strong>"
    toggleEl.addEventListener("click", function(e) {
        if (!document.body.classList.contains("nav-open")) {
            document.body.classList.toggle("nav-open")
            toggleEl.innerHTML = "Close menu"
        } else {
            document.body.classList.toggle("nav-open")
            const activeName = document.querySelector(".menu-container li .active").innerHTML
            toggleEl.innerHTML = `Select category <strong>${activeName}</strong>`
        }
    })

    // Iframe
    const iframeContainerEl = document.createElement("div")
    document.body.insertBefore(iframeContainerEl, document.body.firstChild)
    iframeContainerEl.classList.add("live-iframe")
    // Close btn
    iframeContainerEl.innerHTML = "<div onclick='closeIframe()' class='close-btn'></div>" 
    // Iframe wrap
    const iframeWrapEl = document.createElement("div")
    iframeContainerEl.appendChild(iframeWrapEl)
    iframeWrapEl.classList.add("live-iframe-wrap")
    
    // Populate category names 
    const categories = window.iframeCategories = {"All": {channels:[]}}
    window.iframeData.forEach( item => {
        const itemCategories = item["Categories"].split(",")
        itemCategories.forEach(function ( name ) {
            if ( name ) {
                const existingCategory = categories[ name.trim() ]
                if (!existingCategory) {
                    categories[ name.trim() ] = {channels: [item["#"]]}
                } else { 
                    existingCategory.channels.push(item["#"])
                }
            }
            categories["All"].channels.push(item["#"])
        } )
    })

    // New menu ul
    const menuListEl = document.createElement("ul")
    menuContainerEl.appendChild(menuListEl)
    
    
    // Populate ul items
    addListItems()


    // Add iframe button click listeners
    document.querySelectorAll(".channel-logo").forEach(function(el) {
        const numberEl = el.querySelector(".channel-number")
        const endIndex = numberEl.innerHTML.indexOf("<span")
        const elChannelNumber = numberEl.innerHTML.substring(0, endIndex)
        el.onclick = `openIFrame("${elChannelNumber}")`
    })
    

    
    // Header
    const header = document.createElement("header")
    let headerInnerHTML = ""
    headerInnerHTML += "<div class='sidebar-toggle'>&#9776;</div>"
    
    headerInnerHTML += "<div class='logo'><img src='/live-tv/static/iframe/logo-s.png' alt='logo'/></div>"
    
    headerInnerHTML += "<div><div class='search-container'><input type='search' placeholder='Find a channel' /><ul class='search-results'></ul></div></div>"
    
    headerInnerHTML += "<div class='links'>"
    headerInnerHTML += "<a href='https://eternityready.tv/live-tv#' class='top-link-active'>Live TV</a>"
    headerInnerHTML += "<a href='https://eternityready.tv/on-demand' class='top-link'>On Demand</a>"
    headerInnerHTML += "</div>"
    
    header.innerHTML = headerInnerHTML
    document.body.insertBefore(header, document.body.firstChild)
    
    const sidebar = document.createElement("aside")
    document.body.insertBefore(sidebar, document.body.firstChild)
    const sidebarList = document.createElement("ul")
    sidebar.append(sidebarList)

    // /////////////////////////
    // /////////////////////////
    // /////////////////////////
    // Add items to sidebar

    // let search = document.createElement("li")
    // search.innerHTML = `
    //     <div class="search-container">
    //         <input type="search" placeholder="Find a channel" />
    //         <ul class="search-results"></ul>
    //     </div>`
    // sidebarList.appendChild(search)

    let head1 = document.createElement("li")
    head1.innerHTML = "<h4>WATCH NOW</h4>"
    sidebarList.appendChild(head1)
    
    let item1a = document.createElement("li")
    item1a.innerHTML = `<a href='https://eternityready.tv/live-tv#'>Live TV</a>`
    sidebarList.appendChild(item1a)
    
    let item1b = document.createElement("li")
    item1b.innerHTML = `<a href="https://eternityready.tv/on-demand" target="_blank">On Demand</a>`
    sidebarList.appendChild(item1b)
    
    let head2 = document.createElement("li")
    head2.innerHTML = "<h4>MORE ABOUT ETERNITY READY TV</h4>"
    sidebarList.appendChild(head2)
    // "Live Radio": "https://www.eternityreadyradio.com/player",
    // "Rapture Ready TV": "https://www.raptureready.tv",
    // "Contact us": "https://help.eternityready.com",
    // "Donate": "https://donorbox.org/eternity-ready-radio",
    
    let item2a = document.createElement("li")
    item2a.innerHTML = `<a href="https://www.eternityreadyradio.com/player" target="_blank">Live Radio</a>`
    sidebarList.appendChild(item2a)

    let item2b = document.createElement("li")
    item2b.innerHTML = `<a href="https://www.raptureready.tv" target="_blank">Rapture Ready TV</a>`
    sidebarList.appendChild(item2b)

    let item2c = document.createElement("li")
    item2c.innerHTML = `<a href="https://help.eternityready.com" target="_blank">Contact Us</a>`
    sidebarList.appendChild(item2c)

    let item2d = document.createElement("li")
    item2d.innerHTML = `<a href="https://donorbox.org/eternity-ready-radio" target="_blank">Donate</a>`
    sidebarList.appendChild(item2d)

    let itemLas = document.createElement("li")
    itemLas.innerHTML = `<a href="https://www.eternityreadyradio.com" target="_blank">Music & Podcasts</a>`
    sidebarList.appendChild(itemLas)
    /**
     * google play store image to link @ https://play.google.com/store/apps/details?id=com.wEternityReadyRadio&hl=en_US&gl=US
N
apple store @ https://apps.apple.com/us/app/eternity-ready/id1564486246


     */
    let head3 = document.createElement("li")
    head3.innerHTML = "<h4 class='mb'>MOBILE APPS</h4>"
    sidebarList.appendChild(head3)
    head3.style.paddingTop = "20px"
    
    let item3a = document.createElement("li")
    item3a.innerHTML = `<a href='https://play.google.com/store/apps/details?id=com.wEternityReadyRadio&hl=en_US&gl=US'  class='mb' target="_blank"><img src='/live-tv/static/iframe/google-s.svg' alt='Play Store'/></a>`
    sidebarList.appendChild(item3a)
    item3a.style.marginTop = "20px"
    
    let item3b = document.createElement("li")
    item3b.innerHTML = `<a href="https://apps.apple.com/us/app/eternity-ready/id1564486246"  class='mb'  target="_blank"><img alt='apple store' src='/live-tv/static/iframe/apple-s.svg'  /></a>`
    sidebarList.appendChild(item3b)
    item3b.style.marginTop = "20px"
    

    // const extraItemKeys = Object.keys(extraItems)
    // for (let i = 0; i < extraItemKeys.length; i++) {
    //     const linkName = extraItemKeys[i]
    //     const liEl = document.createElement("li")
    //     liEl.innerHTML = `<a href="${extraItems[linkName]}" target="_blank">${linkName}</a>`
    //     sidebarList.appendChild(liEl)
    // }
    
    const copyright = document.createElement("small")
    copyright.innerHTML = "@2023 Eternity Ready. All rights reserved."
    sidebarList.appendChild(copyright)

    // Overlay
    const overlay = document.createElement("div")
    overlay.classList.add("overlay")
    document.body.insertBefore(overlay, document.body.firstChild)

    // Toggle sidebar listener
    document.body.querySelector(".sidebar-toggle").addEventListener("click", function() {
        document.body.classList.toggle(`sidebar-open`)
        const toggle = document.body.querySelector(".sidebar-toggle")
        if (document.body.classList.contains("sidebar-open")) {
            toggle.innerHTML = "&#9587;"
        } else {
            toggle.innerHTML = "&#9776;"
        }
    })


    function addListItems() {
        
        const ordering = {}
        sortOrder = [
            "All",
            "Top Networks",
            "News + Opinions",
            "Kids & Family",
            "International",
            "Mideast",
            "Bible Prophecy",
            "Lifestyle + Others",
        ]
        
        for (var i=0; i<sortOrder.length; i++) {
            ordering[sortOrder[i]] = i;
        }

        // Each category
        Object.keys(categories).sort((a,b) => {
            return (ordering[a] - ordering[b]) 
        })
        .forEach(name => {
            const liEl = document.createElement("li")
            liEl.innerHTML = `<button data-name='${name}' onclick='onListItemClick("${name}")'>${name}</button>`
            menuListEl.appendChild(liEl)

            if (name === "All") {
                liEl.querySelector("button").classList.add("active") 
            }
        })
    
        

        Object.keys(extraItems).forEach((name, index) => {
            const liEl = document.createElement("li")
            liEl.innerHTML = `<a href="${extraItems[name]}" target="_blank">${name}</a>`
            menuListEl.appendChild(liEl)
            if (index === 0) {
                liEl.classList.add("first-link")
            }
        })

    }

    
}


function resizeIframe(obj) {
    obj.style.height = obj.contentWindow.document.documentElement.scrollHeight + 'px';
}


function openIFrame(number) {	
    //gtag('event', 'event', 'event_category': 'channel', 'event_label': String(number), 'value': 0);
    const wrap = document.querySelector(".live-iframe-wrap")
    wrap.innerHTML = ""

    let foundItem
    
    for (let i = 0; i < window.iframeData.length; i++) {
        const item = window.iframeData[i];
        if (item["#"] === number) {
            foundItem = item
            break
        }
    }

    if (!foundItem ) return 
    const url = foundItem["video embeds for iframe"]
    
    // wrap.innerHTML = `<iframe width="560" height="315" src="https://www.youtube.com/embed/n3EcEYFgyrQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`
    wrap.innerHTML = `<iframe width="560" height="315" src="${url}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`
    wrap.parentElement.classList.add("open")

    window.scrollTo(0, 0)
}

function closeIframe() {
    const wrap = document.querySelector(".live-iframe-wrap")
    wrap.parentElement.classList.remove("open")
    wrap.innerHTML = ""
}

function onListItemClick(categoryName) {

    // Change active category
    document.querySelector(".menu-container li .active").classList.remove("active")
    document.querySelector(`[data-name="${categoryName}"]`).classList.add("active")

    // Change channels list
    const channelsToShow = window.iframeCategories[categoryName].channels

    const nameEls = document.querySelectorAll(".channel-number")
    nameEls.forEach(el => {
        const endIndex = el.innerHTML.indexOf("<span")
        const elChannelNumber = el.innerHTML.substring(0, endIndex)
        // Clear top margin
        // el.parentElement.parentElement.style.marginTop = 0
        let setFirstMargin = false
        if (channelsToShow.includes(elChannelNumber)) {
            if (!setFirstMargin) {
                // el.parentElement.parentElement.style.marginTop = "20px"
                setFirstMargin = true
            }
            el.parentElement.parentElement.classList.remove("cat-hidden")
        } else {
            el.parentElement.parentElement.classList.add("cat-hidden") 
        }
    })

    // Scroll to top 
    const channelsContainer = document.querySelector("#channels-container")
    channelsContainer.scrollTo( channelsContainer.scrollLeft, 0 )
}


// Set timezone of user
(function (window) {
    var d = new Date();
    var n = d.getTimezoneOffset();
    var timezone = n / -60;
    window.GLOBAL_time_offset = -(timezone + 7)
    // window.GLOBAL_time_offset = 0
})(window)

document.addEventListener( "DOMContentLoaded", 
    function() {
        initIframe()
        openIFrame("1")
        setupSearch()
        // $("#channels-container").scrollLeft(240.0*updateTime()+90.0 - 300.0);
        // $("#channels-container").scroll(update_pos);
        // update_pos()
    	// updateTime()
    }
)

function goToSearchResult(title) {
    const searchEl = document.querySelector("input[type=search]")
    const resultsEl = document.querySelector('.search-results')
    resultsEl.classList.remove('open')
    searchEl.value = ""
    
    
    // const toggleEl = document.querySelector('.sidebar-toggle')
    // toggleEl.click()

    if ((window.GLOBAL_channels || []).map(function(channel) {
            return channel.name
        }).includes(title)) {
        focusChannel(title)
    } else if (window.onDemandChannels.includes(title)) {
        window.location.href = "/on-demand?ch=" + title
    }
    // const toggleEl = document.querySelector('.nav-toggle')
    // if (!document.body.classList.contains("nav-open")) {
    //     document.body.classList.toggle("nav-open")
    //     toggleEl.innerHTML = "Close menu"
    // } else {
    //     document.body.classList.toggle("nav-open")
    //     const activeName = document.querySelector(".menu-container li .active").innerHTML
    //     toggleEl.innerHTML = `Select category <strong>${activeName}</strong>`
    // }
    
    return false;

    
    if ((window.GLOBAL_channels || []).map(function(channel) {
            return channel.name
        }).includes(title)) {
        focusChannel(title)
    } 
    // else if (window.liveTvChannels.includes(title)) {
    //     window.location.href = "/live-tv?ch=" + title
    // }
}



function setupSearch() {
    const searchEl = document.querySelector("input[type=search]")
    const resultsEl = document.querySelector('.search-results')
    
    searchEl.addEventListener("input", function(e) {
        resultsEl.innerHTML = ""
        resultsEl.classList.remove('open')

        if (!e.target.value) return
        const query = e.target.value.toLowerCase()
        let allTitles = (window.GLOBAL_channels || []).map(function(channel) {
            return channel.name
        })
        allTitles = allTitles.concat(window.onDemandChannels || [])
        const resultTitles = allTitles
            .filter(title => title.toLowerCase().includes(query))
        
        if (!resultTitles.length) return
        const resultElsHtml = resultTitles
            .map( title => `<li tabindex="-1" onclick="goToSearchResult('${title}')">${title}</li>`)
        resultsEl.innerHTML = resultElsHtml.join("")
        resultsEl.classList.add('open')
    })
    
    searchEl.addEventListener("blur", function(e) {
        const clickedResult = resultsEl.contains(e.relatedTarget)
        if (clickedResult) return
        resultsEl.classList.remove('open')
    })

    searchEl.addEventListener("focus", function() {
        resultsEl.classList.add('open')
    })
}



// Note: add_channel is redefined
function add_channel(chan) {
	var number = $("<div/>").addClass("channel-number").text(chan.number);
	number.append($("<span/>").addClass("channel-name").text(chan.name))
	var name = $("<div/>").addClass("channel-name").text(chan.name);
	var logo = $("<div/>").addClass("channel-logo").append(number);
	logo.css("background-image", "url('static/img/logos_2/" + chan.number + ".jpg')");
	// var dummy = $("<div/>").addClass("channel-logo-dummy");
	var programs = $("<div/>").addClass("programs");
	var display_name = "Test " + chan.name + " Show";
	if (display_name.length >= 25) {
		display_name = display_name.substring(0, 20) + "...";
	}
	var channel = $("<div/>").addClass("channel").attr("data-next-pos", 0);
	logo.appendTo(channel);
	// dummy.appendTo(channel);
	programs.appendTo(channel);
	channel.appendTo($("#channels-container"));
	chan.element = channel;
    // New code
    channel.get(0).addEventListener("click" ,function() {
        openIFrame(chan.number)
    })
    // END New code
	populate_channel(chan, channel);
}

