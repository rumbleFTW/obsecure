function censorImage(imgNode, className) {
    const originalParent = imgNode.parentElement;
    imgNode.style.filter = 'blur(30px)';
    const container = document.createElement('div');
    container.style.position = 'relative';
    container.style.textAlign = 'center';
    container.style.color = 'white';
    const text = document.createElement('div');
    text.className = 'overlay';
    text.style.position = 'absolute';
    text.style.top = '50%';
    text.style.left = '50%';
    text.style.transform = 'translate(-50%, -50%)';
    text.style.fontSize = '34px';
    text.style.fontFamily = 'Google Sans,sans-serif';
    text.style.fontWeight = '700';
    text.style.color = 'white';
    text.style.lineHeight = '1em';
    text.style['-webkit-text-fill-color'] = 'white';
    text.style['-webkit-text-stroke-width'] = '1px';
    text.style['-webkit-text-stroke-color'] = 'black';
    originalParent.insertBefore(container, imgNode);
    container.appendChild(imgNode);
    container.appendChild(text);
    text.textContent = `${className}\n⚠️`;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if(message.type == 'init') {
        const imageUrls = [];
        const imgs = [...document.getElementsByTagName('img')];
        for(let i = 0; i<imgs.length; i++) {
            if(imgs[i].width > 244 && imgs[i].height > 244) {
                imageUrls.push(imgs[i].src);
            }
        }
        if(imageUrls.length > 0) chrome.runtime.sendMessage({data: imageUrls}, async function(response) {
            for(const src of Object.keys(response.data)) {
                const imgElement = document.querySelector(`img[src="${src}"]`);
                censorImage(imgElement, response.data[src]);
            }
        });
        return true;
    }
});