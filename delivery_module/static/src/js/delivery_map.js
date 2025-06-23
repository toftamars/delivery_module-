odoo.define('delivery_module.delivery_map', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var fieldRegistry = require('web.field_registry');
    var core = require('web.core');

    var QWeb = core.qweb;

    var DeliveryMapWidget = AbstractField.extend({
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
                self._createWidget();
                self._initMap();
            });
        },

        _createWidget: function () {
            // Widget'ı manuel olarak oluştur
            this.el.innerHTML = 
                '<div class="delivery_map_widget" style="padding: 10px;">' +
                    '<div class="route-info alert alert-info" style="margin-bottom: 10px; padding: 10px; border-radius: 4px;">' +
                        '<strong>Rota Bilgileri:</strong> Yükleniyor...' +
                    '</div>' +
                    '<div class="delivery-map-container" style="height: 400px; width: 100%; border: 1px solid #ccc; border-radius: 4px; position: relative; background-color: #f8f9fa; min-height: 400px;">' +
                        '<div style="display: flex; align-items: center; justify-content: center; height: 100%;">' +
                            '<div class="text-muted">' +
                                '<i class="fa fa-map-marker" style="font-size: 2em; margin-bottom: 10px;"></i>' +
                                '<br>' +
                                'Harita yükleniyor...' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>';
        },

        _initMap: function () {
            var self = this;
            var record = this.recordData;
            
            // Rota bilgilerini güncelle
            this._updateRouteInfo();
            
            // Koordinatlar varsa haritayı yükle
            if (record.start_latitude && record.start_longitude && 
                record.end_latitude && record.end_longitude) {
                this._loadMap();
            } else {
                this._showNoDataMessage();
            }
        },

        _updateRouteInfo: function () {
            var record = this.recordData;
            var infoContainer = this.el.querySelector('.route-info');
            
            if (infoContainer) {
                if (record.route_distance && record.route_duration) {
                    infoContainer.innerHTML = '<strong>Rota Bilgileri:</strong> ' +
                        'Mesafe: ' + record.route_distance + ' km, ' +
                        'Süre: ' + record.route_duration + ' dakika';
                    infoContainer.className = 'route-info alert alert-success';
                } else {
                    infoContainer.innerHTML = '<strong>Rota Bilgileri:</strong> Koordinat bilgisi eksik';
                    infoContainer.className = 'route-info alert alert-warning';
                }
            }
        },

        _showNoDataMessage: function () {
            var container = this.el.querySelector('.delivery-map-container');
            if (container) {
                container.innerHTML = '<div style="display: flex; align-items: center; justify-content: center; height: 100%;">' +
                    '<div class="text-muted">' +
                    '<i class="fa fa-exclamation-triangle" style="font-size: 2em; margin-bottom: 10px;"></i>' +
                    '<br>Koordinat bilgisi bulunamadı' +
                    '</div></div>';
            }
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
                    self._createMap();
                };
                script.onerror = function () {
                    self._showMapError();
                };
                document.head.appendChild(script);
            } else {
                self._createMap();
            }
        },

        _createMap: function () {
            var record = this.recordData;
            var mapContainer = this.el.querySelector('.delivery-map-container');
            
            if (!mapContainer || typeof L === 'undefined') {
                this._showMapError();
                return;
            }

            try {
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

                // Basit rota çiz
                var routeCoords = [
                    [record.start_latitude, record.start_longitude],
                    [record.end_latitude, record.end_longitude]
                ];
                
                this.route = L.polyline(routeCoords, {
                    color: 'blue',
                    weight: 4,
                    opacity: 0.7
                }).addTo(this.map);

                // Haritayı rota sığacak şekilde ayarla
                this.map.fitBounds(this.route.getBounds(), {padding: [20, 20]});
                
            } catch (error) {
                console.error('Harita oluşturma hatası:', error);
                this._showMapError();
            }
        },

        _showMapError: function () {
            var container = this.el.querySelector('.delivery-map-container');
            if (container) {
                container.innerHTML = '<div style="display: flex; align-items: center; justify-content: center; height: 100%;">' +
                    '<div class="text-danger">' +
                    '<i class="fa fa-exclamation-circle" style="font-size: 2em; margin-bottom: 10px;"></i>' +
                    '<br>Harita yüklenemedi' +
                    '</div></div>';
            }
        }
    });

    fieldRegistry.add('delivery_map', DeliveryMapWidget);

    return DeliveryMapWidget;
}); 