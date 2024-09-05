chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
	if (message.action === "fuzzV1") {
		document.body.style.cursor = 'crosshair';
		const forms = document.querySelectorAll("form");
		forms.forEach(form => {
			form.addEventListener("click", function () {
				const action = form.getAttribute('action');
				const absoluteActionUrl = new URL(action, window.location.href).href;
				const inputs = form.querySelectorAll("input");
				const names = [];
				for (const inp of inputs) {
					const type = inp.getAttribute("type") || "text";
					if (type === "text" || type == "password" || type === "email" || type === "url") {
						names.push(inp.getAttribute("name"));
					}
				}
				alert(absoluteActionUrl);
				chrome.runtime.sendMessage({ action: "fuzzResponse", link: absoluteActionUrl, params: names });
				document.body.style.cursor = '';

			})
		})
	}
})
