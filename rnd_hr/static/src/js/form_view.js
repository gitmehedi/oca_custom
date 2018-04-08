odoo.define("rnd_hr.form_view2", function (require) {
    "use strict";

    var FormView = require("web.FormView");
    FormView.include({

        load_record: function (record) {
            var self = this;
            self._super.apply(this, arguments);
            if (self.model == 'rnd.rostering') {
                this.append_org_chart(record);
            }
            ;
        },

        append_org_chart: function (record) {
            var self = this;
            var record_id = record.id;

            var employee = 'employee="' + record_id + '">';
            var $new_div = '<div id="people" ' + employee+'</div>';
            var str = '<div style="width: 90%;"><canvas style="display:none;" id="canvas"></canvas>' + $new_div + '</div>';

            var $peopleDiv = self.$el.find('#mygraph').replaceWith(str);
        },

    });
});