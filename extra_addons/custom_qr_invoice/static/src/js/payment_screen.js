/** @odoo-module **/
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

patch(PaymentScreen.prototype, {
    async onClickBoleta() {
        const order = this.pos.get_order();
        const total = order ? order.get_total_with_tax() : 0;
        this.popup.add(ErrorPopup, {
            title: "Información de Boleta",
            body: `El monto total a pagar es: S/ ${total.toFixed(2)}`,
        });
    }
});