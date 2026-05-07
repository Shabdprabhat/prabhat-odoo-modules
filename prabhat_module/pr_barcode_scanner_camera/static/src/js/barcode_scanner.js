odoo.define('pr_barcode_scanner.camera', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');
    var Dialog = require('web.Dialog');

    var BarcodeScannerWidget = Widget.extend({
        template: 'barcode_scanner_template',
        
        init: function(parent, options) {
            this._super(parent);
            this.options = options || {};
        },
        
        start: function() {
            this.initCamera();
        },
        
        initCamera: function() {
            var self = this;
            var video = this.$el.find('#barcode_video')[0];
            
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
                    .then(function(stream) {
                        video.srcObject = stream;
                        video.play();
                        self.startBarcodeDetection(video);
                    })
                    .catch(function(err) {
                        self.showError('Camera error: ' + err.message);
                    });
            } else {
                this.showError('Camera not supported in this browser');
            }
        },
        
        startBarcodeDetection: function(video) {
            var self = this;
            
            if ('BarcodeDetector' in window) {
                var barcodeDetector = new BarcodeDetector({
                    formats: ['ean_13', 'ean_8', 'upc_a', 'upc_e', 'code_128', 'code_39', 'qr_code']
                });
                
                var detectLoop = setInterval(function() {
                    if (video.readyState === video.HAVE_ENOUGH_DATA) {
                        barcodeDetector.detect(video).then(function(barcodes) {
                            if (barcodes.length > 0) {
                                clearInterval(detectLoop);
                                self.onBarcodeDetected(barcodes[0].rawValue);
                            }
                        }).catch(function(err) {
                            console.log('Barcode detection error:', err);
                        });
                    }
                }, 500);
            } else {
                this.showError('Barcode Detection API not supported');
            }
        },
        
        onBarcodeDetected: function(barcode) {
            var self = this;
            
            this._rpc({
                model: 'barcode.scan',
                method: 'action_search_product',
                args: [barcode]
            }).then(function(result) {
                if (result.error) {
                    self.showError(result.error);
                } else {
                    self.do_action({
                        type: 'ir.actions.client',
                        tag: 'display_notification',
                        params: {
                            'title': 'Product Found',
                            'message': result.product_name + ' - ' + result.product_price,
                            'type': 'success'
                        }
                    });
                    self.destroy();
                }
            });
        },
        
        showError: function(message) {
            Dialog.alert(this, 'Error', message);
        },
    });

    return BarcodeScannerWidget;
});