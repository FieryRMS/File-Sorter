
const viewer = new ImageViewer.FullScreenViewer({
    hasZoomButtons:false
});

const OpenImage = (uri)=>{
    viewer.show(uri)
}

const urlParams = new URLSearchParams(window.location.search);
if(urlParams.get("file")){
    OpenImage(urlParams.get("file"))
}