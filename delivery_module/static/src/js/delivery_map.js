odoo.define('delivery_module.delivery_map', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var fieldRegistry = require('web.field_registry');
    var core = require('web.core');

    var QWeb = core.qweb;

    var DeliveryMapWidget = AbstractField.extend({
        template: 'delivery_map_template',
        supportedFieldTypes: ['char'],
        
        init: function () {
            this._super.apply(this, arguments);
            this.map = null;
            this.markers = [];
            this.route = null;
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._loadMap();
            });
        },

        _loadMap: function () {
            var self = this;
            
            // Leaflet CSS'ini yükle
            if (!document.querySelector('link[href*="leaflet.css"]')) {
                var link = document.createElement('link');
                link.rel = 'stylesheet';
                link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
                document.head.appendChild(link);
            }

            // Leaflet JS'ini yükle
            if (typeof L === 'undefined') {
                var script = document.createElement('script');
                script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
                script.onload = function () {
                    self._initMap();
                };
                document.head.appendChild(script);
            } else {
                self._initMap();
            }
        },

        _initMap: function () {
            var self = this;
            var record = this.recordData;
            
            if (!record.start_latitude || !record.start_longitude || !record.end_latitude || !record.end_longitude) {
                return;
            }

            // Harita container'ını oluştur
            var mapContainer = this.el.querySelector('.delivery-map-container');
            if (!mapContainer) {
                return;
            }

            // Haritayı başlat
            this.map = L.map(mapContainer).setView([record.start_latitude, record.start_longitude], 12);

            // OpenStreetMap tile layer
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(this.map);

            // Başlangıç noktası (depo)
            var startMarker = L.marker([record.start_latitude, record.start_longitude])
                .addTo(this.map)
                .bindPopup('<b>Depo</b><br>Başlangıç noktası');

            // Hedef noktası (müşteri)
            var endMarker = L.marker([record.end_latitude, record.end_longitude])
                .addTo(this.map)
                .bindPopup('<b>Müşteri</b><br>' + (record.delivery_address || 'Teslimat adresi'));

            this.markers = [startMarker, endMarker];

            // Rota çiz
            this._drawRoute();
            
            // Kontrol butonlarını ekle
            this._addRouteControls();
        },

        _drawRoute: function () {
            var self = this;
            var record = this.recordData;
            
            // OSRM API'den gerçek rota al
            this._getOSRMRoute().then(function(routeData) {
                if (routeData && routeData.coordinates && routeData.coordinates.length > 0) {
                    // Gerçek rota koordinatlarını kullan
                    var routeCoords = routeData.coordinates.map(function(coord) {
                        return [coord[1], coord[0]]; // GeoJSON format: [lon, lat] -> Leaflet format: [lat, lon]
                    });
                    
                    self.route = L.polyline(routeCoords, {
                        color: 'blue',
                        weight: 4,
                        opacity: 0.7
                    }).addTo(self.map);
                    
                    // Rota bilgilerini güncelle
                    self._updateRouteInfo(routeData.distance, routeData.duration);
                    
                    // Rota talimatlarını göster
                    self._showRouteInstructions(routeData.steps);
                } else {
                    // Fallback: Basit düz çizgi rota
                    var routeCoords = [
                        [record.start_latitude, record.start_longitude],
                        [record.end_latitude, record.end_longitude]
                    ];
                    
                    self.route = L.polyline(routeCoords, {
                        color: 'red',
                        weight: 3,
                        opacity: 0.5,
                        dashArray: '5, 10'
                    }).addTo(self.map);
                    
                    self._updateRouteInfo(record.route_distance, record.route_duration);
                }
                
                // Haritayı rota sığacak şekilde ayarla
                self.map.fitBounds(self.route.getBounds(), {padding: [20, 20]});
            });
        },

        _getOSRMRoute: function () {
            var self = this;
            var record = this.recordData;
            
            return new Promise(function(resolve, reject) {
                if (!record.start_latitude || !record.start_longitude || 
                    !record.end_latitude || !record.end_longitude) {
                    resolve(null);
                    return;
                }
                
                // OSRM API çağrısı
                var url = "http://router.project-osrm.org/route/v1/driving/" +
                    record.start_longitude + "," + record.start_latitude + ";" +
                    record.end_longitude + "," + record.end_latitude;
                
                var params = {
                    overview: 'full',
                    geometries: 'geojson',
                    steps: 'true'
                };
                
                // URL parametrelerini ekle
                var queryString = Object.keys(params).map(function(key) {
                    return key + '=' + encodeURIComponent(params[key]);
                }).join('&');
                
                url += '?' + queryString;
                
                fetch(url)
                    .then(function(response) {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(function(data) {
                        if (data.code === 'Ok' && data.routes && data.routes.length > 0) {
                            var route = data.routes[0];
                            resolve({
                                coordinates: route.geometry.coordinates,
                                distance: route.distance / 1000, // km
                                duration: route.duration / 60,   // dakika
                                steps: route.legs[0].steps
                            });
                        } else {
                            resolve(null);
                        }
                    })
                    .catch(function(error) {
                        console.warn('OSRM API hatası:', error);
                        resolve(null);
                    });
            });
        },

        _updateRouteInfo: function (distance, duration) {
            var infoContainer = this.el.querySelector('.route-info');
            
            if (infoContainer) {
                var routeType = distance ? 'Gerçek Rota' : 'Tahmini Rota';
                var colorClass = distance ? 'alert-success' : 'alert-warning';
                
                infoContainer.innerHTML = `
                    <div class="alert ${colorClass}">
                        <strong>${routeType} Bilgileri:</strong><br>
                        Mesafe: ${distance || this.recordData.route_distance} km<br>
                        Tahmini Süre: ${duration || this.recordData.route_duration} dakika
                    </div>
                `;
            }
        },

        _showRouteInstructions: function (steps) {
            var instructionsContainer = this.el.querySelector('.route-instructions');
            
            if (instructionsContainer && steps && steps.length > 0) {
                var instructionsHtml = '<div class="alert alert-info"><strong>Rota Talimatları:</strong><ul>';
                
                steps.forEach(function(step, index) {
                    if (step.maneuver && step.maneuver.instruction) {
                        instructionsHtml += '<li>' + step.maneuver.instruction + '</li>';
                    }
                });
                
                instructionsHtml += '</ul></div>';
                instructionsContainer.innerHTML = instructionsHtml;
            }
        },

        _addRouteControls: function () {
            var self = this;
            
            // Rota kontrol butonları
            var routeControls = L.control({position: 'topright'});
            
            routeControls.onAdd = function (map) {
                var div = L.DomUtil.create('div', 'route-controls');
                div.innerHTML = `
                    <div class="btn-group-vertical" role="group">
                        <button class="btn btn-sm btn-primary" id="refresh-route" title="Rotayı Yenile">
                            <i class="fa fa-refresh"></i>
                        </button>
                        <button class="btn btn-sm btn-info" id="show-instructions" title="Talimatları Göster">
                            <i class="fa fa-list"></i>
                        </button>
                        <button class="btn btn-sm btn-success" id="fullscreen-map" title="Tam Ekran">
                            <i class="fa fa-expand"></i>
                        </button>
                    </div>
                `;
                
                // Event listeners
                div.querySelector('#refresh-route').onclick = function() {
                    self._refreshRoute();
                };
                
                div.querySelector('#show-instructions').onclick = function() {
                    self._toggleInstructions();
                };
                
                div.querySelector('#fullscreen-map').onclick = function() {
                    self._toggleFullscreen();
                };
                
                return div;
            };
            
            routeControls.addTo(this.map);
        },

        _refreshRoute: function () {
            if (this.route) {
                this.map.removeLayer(this.route);
            }
            this._drawRoute();
        },

        _toggleInstructions: function () {
            var instructionsContainer = this.el.querySelector('.route-instructions');
            if (instructionsContainer) {
                instructionsContainer.style.display = 
                    instructionsContainer.style.display === 'none' ? 'block' : 'none';
            }
        },

        _toggleFullscreen: function () {
            var mapContainer = this.el.querySelector('.delivery-map-container');
            if (mapContainer) {
                if (mapContainer.classList.contains('fullscreen')) {
                    mapContainer.classList.remove('fullscreen');
                    mapContainer.style.position = 'relative';
                    mapContainer.style.height = '400px';
                } else {
                    mapContainer.classList.add('fullscreen');
                    mapContainer.style.position = 'fixed';
                    mapContainer.style.top = '0';
                    mapContainer.style.left = '0';
                    mapContainer.style.width = '100vw';
                    mapContainer.style.height = '100vh';
                    mapContainer.style.zIndex = '9999';
                }
                
                // Haritayı yeniden boyutlandır
                if (this.map) {
                    this.map.invalidateSize();
                }
            }
        },

        destroy: function () {
            if (this.map) {
                this.map.remove();
            }
            this._super.apply(this, arguments);
        }
    });

    fieldRegistry.add('delivery_map', DeliveryMapWidget);

    return DeliveryMapWidget;
}); 