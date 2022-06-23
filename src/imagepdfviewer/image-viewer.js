
const viewer = new ImageViewer.FullScreenViewer({
    hasZoomButtons: false
});

const OpenImage = (uri) => {
    viewer.show(uri);
    PDFViewerApplication.close();
    document.getElementsByTagName("BODY")[0].style.display = "initial";
};
const OpenPdf = (uri) => {
    PDFViewerApplication.open(uri);
    document.getElementsByTagName("BODY")[0].style.display = "initial";
    viewer.hide();
};

const HideAll = () => {
    PDFViewerApplication.close();
    document.getElementsByTagName("BODY")[0].style.display = "none";
    viewer.hide();
}