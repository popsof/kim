
function applyUrl() {
	var url = document.getElementById("id_url").value
	var res = /www\.youtube\.com\/watch\?v=([-\w]+)/.exec(url)

//	alert( url + " " + res[1] )
	if( !res || !res[1] )
		alert( "Wrong youtube url!!!" )

	var panel = document.getElementById("id_preview_panel")
	panel.innerHTML = 
		"<iframe class=\"embed-responsive-item\" src=\"https://www.youtube.com/embed/" + res[1] + "\" allowfullscreen></iframe>"
}

