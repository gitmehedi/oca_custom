odoo.define('payment_checkout.checkout', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;
    var qweb = core.qweb;
    ajax.loadXML('/payment_checkout/static/src/xml/checkout_templates.xml', qweb);

    // The following currencies are integer only, see
    // https://checkout.com/docs/currencies#zero-decimal
    var int_currencies = [
        'BIF', 'XAF', 'XPF', 'CLP', 'KMF', 'DJF', 'GNF', 'JPY', 'MGA', 'PYGí',
        'RWF', 'KRW', 'VUV', 'VND', 'XOF'



    window.CKOConfig = {
        publicKey: 'pk_test_cfca8527-43c3-454b-bc03-32a6903acf69',
        paymentToken: 'pay_tok_SPECIMEN-000',
        customerEmail: 'user@email.com',
        value: 100,
        currency: 'EUR',
        cardFormMode: Checkout.CardFormModes.CARD_CHARGE,
        paymentMode: 'cards' || 'mixed' || 'localpayments',
        countryCode: 'DE',
        renderMode: 0 || 1 || 2 || 3,
        buttonLabel: 'BUY NOW',
        widgetColor: '#123123',
        buttonColor: '#123123',
        buttonLabelColor: '#123123',
        title: 'Merchant',
        subtitle: 'Merchant Subtitle',
        logoUrl: 'https://docs.checkout.com/img/merchant-logo.png',
        formButtonLabel: 'Complete Purchase',
        theme: 'light',
        cardTokenised: function (event) {
            console.log(event.data.cardToken);
            document.getElementsByClassName('payment-form')[0].submit();
        },
    };
};

var handler = CheckoutCheckout.configure({
    key: $("input[name='checkout_key']").val(),
    image: $("input[name='checkout_image']").val(),
    locale: 'auto',
    closed: function () {
        if (!handler.isTokenGenerate) {
            $('#pay_checkout')
                .removeAttr('disabled')
                .find('i').remove();
        }
    },
    token: function (token, args) {
        handler.isTokenGenerate = true;
        ajax.jsonRpc("/payment/checkout/create_charge", 'call', {
            tokenid: token.id,
            email: token.email,
            amount: $("input[name='amount']").val(),
            acquirer_id: $("#acquirer_checkout").val(),
            currency: $("input[name='currency']").val(),
            invoice_num: $("input[name='invoice_num']").val(),
            return_url: $("input[name='return_url']").val()
        }).done(function (data) {
            handler.isTokenGenerate = false;
            window.location.href = data;
        }).fail(function () {
            var msg = arguments && arguments[1] && arguments[1].data && arguments[1].data.message;
            var wizard = $(qweb.render('checkout.error', {'msg': msg || _t('Payment error')}));
            wizard.appendTo($('body')).modal({'keyboard': true});
        });
    },
});

$('#pay_checkout').on('click', function (e) {
    console.log("This is a test");
    // Open Checkout with further options
    alert("Pay Checkout");
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
            window.CKOConfig;

        });
    }
});
})
;
