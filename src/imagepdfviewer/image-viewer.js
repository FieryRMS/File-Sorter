
const viewer = new ImageViewer.FullScreenViewer({
    hasZoomButtons: false
});

const OpenImage = (uri) => {
    viewer.show(uri);
    PDFViewerApplication.close();
};
const OpenPdf = (uri) => {
    PDFViewerApplication.open(uri);
    viewer.hide();
}