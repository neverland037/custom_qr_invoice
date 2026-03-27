/** @odoo-module **/
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

patch(ProductScreen.prototype, {
    async clickProduct(product) {
        if (parseFloat(product.lst_price || 0) <= 0) {
            return this.popup.add(ErrorPopup, {
                title: "Alerta de Precio S/ 0.00",
                body: `El producto "${product.display_name}" tiene precio cero.`,
            });
        }
        return super.clickProduct(...arguments);
    }
});