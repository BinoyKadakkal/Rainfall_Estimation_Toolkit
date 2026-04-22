from PyQt5.QtWebEngineWidgets import QWebEngineView

class MapView(QWebEngineView):

    def __init__(self):
        super().__init__()
        self.load_map()

    def load_map(self):

        html = """
        <html>
        <head>
            <meta charset="utf-8" />

            <link rel="stylesheet"
            href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css"/>

            <script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"></script>
        </head>

        <body style="margin:0;">
            <div id="map" style="width:100%; height:100%;"></div>

            <script>
            var map = L.map('map').setView([10, 76], 6);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: 'OSM'
            }).addTo(map);

            window.addLayer = function(img, bounds){
                L.imageOverlay(img, bounds).addTo(map);
            }
            </script>
        </body>
        </html>
        """

        self.setHtml(html)

    def add_layer(self, image_path):

        bounds = [[8,74],[12,78]]

        js = f"""
        window.addLayer("file:///{image_path}", {bounds});
        """

        self.page().runJavaScript(js)
