odoo.define('payment_checkout.checkout', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;
    var qweb = core.qweb;
    ajax.loadXML('/payment_checkout/static/src/xml/checkout_templates.xml', qweb);

    // The following currencies are integer only, see
    // https://stripe.com/docs/currencies#zero-decimal
    var int_currencies = [
        'BIF', 'XAF', 'XPF', 'CLP', 'KMF', 'DJF', 'GNF', 'JPY', 'MGA', 'PYGí',
        'RWF', 'KRW', 'VUV', 'VND', 'XOF'
    ];

    window.CKOConfig = {
        publicKey: 'pk_test_cfca8527-43c3-454b-bc03-32a6903acf69',
        customerEmail: 'user@email.com',
        value: 100,
        currency: 'EUR',
        cardFormMode: 'cardTokenisation',
        cardTokenised: function (event) {
            console.log(data.event.cardToken);
        }
    };
    $('#pay_checkout').on('click', function (e) {
        // Open Checkout with further options

        if (!$(this).find('i').length)
            $(this).append('<i class="fa fa-spinner fa-spin"/>');
        $(this).attr('disabled', 'disabled');

        var $form = $(e.currentTarget).parents('form');
        var acquirer_id = $(e.currentTarget).closest('div.oe_sale_acquirer_button,div.oe_quote_acquirer_button,div.o_website_payment_new_payment');
        acquirer_id = acquirer_id.data('id') || acquirer_id.data('acquirer_id');
        if (!acquirer_id) {
            return false;
        }

        var so_token = $("input[name='token']").val();
        var so_id = $("input[name='return_url']").val().match(/quote\/([0-9]+)/) || undefined;
        if (so_id) {
            so_id = parseInt(so_id[1]);
        }

        e.preventDefault();
        if ($('.o_website_payment').length !== 0) {
            var currency = $("input[name='currency']").val();
            var amount = parseFloat($("input[name='amount']").val() || '0.0');
            if (!_.contains(int_currencies, currency)) {
                amount = amount * 100;
            }

            ajax.jsonRpc('/website_payment/transaction', 'call', {
                reference: $("input[name='invoice_num']").val(),
                amount: amount,
                currency_id: currency,
                acquirer_id: acquirer_id
            })
            handler.open({
                name: $("input[name='merchant']").val(),
                description: $("input[name='invoice_num']").val(),
                currency: currency,
                amount: amount,
            });
        } else {
            var currency = $("input[name='currency']").val();
            var amount = parseFloat($("input[name='amount']").val() || '0.0');
            if (!_.contains(int_currencies, currency)) {
                amount = amount * 100;
            }

            ajax.jsonRpc('/shop/payment/transaction/' + acquirer_id, 'call', {
                so_id: so_id,
                so_token: so_token
            }, {'async': false}).then(function (data) {
                $form.html(data);
                alert(data);
                var token = window.CKOConfig;
                alert(token);

                // handler.open({
                //     name: $("input[name='merchant']").val(),
                //     description: $("input[name='invoice_num']").val(),
                //     currency: currency,
                //     amount: amount,
                // });
            });
        }
    });
});
