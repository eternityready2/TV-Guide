
setupSidebarToggle()
focusQueriedChannel()
setupSearch()

window.liveTvChannels = []
getLiveTvChannels()

function onListItemClick(channelTitle) {
    const initialIframeHtml = `<iframe 
        width="560" 
        height="315"
        src=""
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
    ></iframe>`

    const channelEl = document.querySelector('[data-channel="' + channelTitle + '"]')
    const iframeCodeEl = channelEl.querySelector('.iframe-code')

    const iframeEl = document.querySelector('.live-iframe-wrap iframe')
    if (iframeCodeEl.innerHTML.trim().startsWith('http')) {
        iframeEl.innerHTML = initialIframeHtml
        iframeEl.src = iframeCodeEl.innerHTML.trim()
    } else if (iframeCodeEl.innerText.trim().startsWith('<iframe')){
        iframeEl.parentElement.innerHTML = iframeCodeEl.innerText.trim()
        iframeEl.width = 560
        iframeEl.height = 315
        iframeEl.frameborder = "0"
        iframeEl.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        iframeEl.allowfullscreen = 'allowfullscreen'
    }

    window.scrollTo(0, 0)
}

function onCategoryClick(category) {
    const categoryGridEl = document.querySelector('[data-category="' + category + '"]')
    categoryGridEl.scrollIntoView({behavior: 'smooth'})
    toggleCategories()
}

function toggleCategories() {
    const categoriesEl = document.querySelector('.categories')
    categoriesEl.classList.toggle('open')
}

function toggleSidebar() {
    document.body.classList.toggle(`sidebar-open`)
    const toggle = document.body.querySelector(".sidebar-toggle")
    if (document.body.classList.contains("sidebar-open")) {
        toggle.innerHTML = "&#9587;"
    } else {
        toggle.innerHTML = "&#9776;"
    }
}

function setupSidebarToggle() {
    document.body.querySelector(".sidebar-toggle").addEventListener("click", toggleSidebar)
}

function focusChannel(title) {
    const channelEl = document.querySelector('[data-channel="' + title + '"]')
    if (!channelEl) return
    channelEl.scrollIntoView({behavior: 'smooth'})
    channelEl.focus()
}

function focusQueriedChannel() {
    const urlSearchParams = new URLSearchParams(window.location.search)
    if (!urlSearchParams.has('ch')) return
    const channelTitle = urlSearchParams.get('ch')
    focusChannel(channelTitle)
}


function setupSearch() {
    const searchEl = document.querySelector("input[type=search]")
    const resultsEl = document.querySelector('.search-results')
    
    searchEl.addEventListener("input", function(e) {
        resultsEl.innerHTML = ""
        resultsEl.classList.remove('open')

        if (!e.target.value) return
        const query = e.target.value.toLowerCase()
        const allTitles = window.onDemandChannelTitles.concat(window.liveTvChannels)
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

function goToSearchResult(title) {
    const searchEl = document.querySelector("input[type=search]")
    const resultsEl = document.querySelector('.search-results')
    resultsEl.classList.remove('open')
    searchEl.value = ""
    // toggleSidebar()
    if (window.onDemandChannelTitles.includes(title)) {
        focusChannel(title)
    } else if (window.liveTvChannels.includes(title)) {
        window.location.href = "/live-tv?ch=" + title
    }
}

function slideLeft(e) {
    const arrowEr = e.target
    const channelsContainer = arrowEr.nextElementSibling.nextElementSibling
    channelsContainer.scrollBy({
        top: 0,
        left: -220,
        behavior: 'smooth'
    })
}

function slideRight(e) {
    const arrowEr = e.target
    const channelsContainer = arrowEr.nextElementSibling
    channelsContainer.scrollBy({
        top: 0,
        left: 220,
        behavior: 'smooth'
    })
}

async function getLiveTvChannels() {
    try {
        const response = await fetch('/live-tv/proxy/channels', {mode: 'no-cors'})
        const data = await response.json()
        window.liveTvChannels = data.channels.map(channel => channel.name)
    } catch (error) {
        window.liveTvChannels = []
    }
}



function initIframe(){
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
    

    // Add iframe button click listeners
    document.querySelectorAll(".channel-logo").forEach(function(el) {
        const numberEl = el.querySelector(".channel-number")
        const endIndex = numberEl.innerHTML.indexOf("<span")
        const elChannelNumber = numberEl.innerHTML.substring(0, endIndex)
        el.onclick = `openIFrame("${elChannelNumber}")`
    })
    
 
    
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

function onListItemClickOld(categoryName) {

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


 
document.addEventListener( "DOMContentLoaded", 
    function() {
        // initIframe()
        // openIFrame("1")
    }
)

 