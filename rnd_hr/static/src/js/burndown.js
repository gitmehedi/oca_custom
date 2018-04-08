odoo.define('rnd_hr.imp_graph', function (require) {
    "use strict";

    var form_widget = require('web.form_widgets');
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var QWeb = core.qweb;


    var ImpGraph = form_widget.WidgetButton.include({
        empID: 0,
        sprint: ["Sunday", "Monday", "Tueday", "Wednesday", "Thusday", "Friday", "Saturday"],
        remainingHours: 40,
        actualBurnData: [],
        averageBurnValue: 0,
        expectedBurnValue: 0,
        startWork: 0,
        sprintLength: function () {
            return this.sprint.length;
        },
        actualBurnDays: function () {
            return this.actualBurnData.length;
        },
        remainingDay: function () {
            return (this.sprintLength() - this.actualBurnDays());
        },
        actualData: function () {
            return this.generageActualData();
        },
        averageData: function () {
            return this.generateAverageData();
        },
        expectedData: function () {
            return this.generateExpectedData();
        },
        on_click: function () {
            var self = this;
            // new Dialog(this, {
            //
            //     title: "MEHEDI ",
            //     // $content: QWeb.render('CrashManager.warning'),
            // }).open();

            if (self.node.attrs.custom === "click") {
                var peopleElement = document.getElementById("people");
                self.empID = peopleElement.getAttribute('employee');
                var element = document.getElementById("canvas");
                if (element.style.display === "none") {
                    element.style.display = "block";
                    self.getDatas();
                } else {
                    element.style.display = "none";
                }
            } else {
                this._super();
            }
        },
        load_apps: function (data) {
            var resData = JSON.parse(data)
            this.actualBurnData = resData.values;
            this.empID = 0;

            var ctx = document.getElementById("canvas").getContext("2d");
            window.myBar = new Chart(ctx, {
                type: 'bar',
                data: this.ChartData(),
                options: {
                    responsive: true,
                    title: {
                        display: true,
                        text: 'Burndown Chart'
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                max: this.remainingHours,
                                min: 0,
                            },
                            display: true,
                            scaleLabel: {
                                display: true,
                                labelString: 'Hours'
                            }
                        }]
                    },
                    tooltips: {
                        enabled: true,
                        mode: 'single',
                        callbacks: {
                            label: function (tooltipItems, data) {
                                switch (tooltipItems.datasetIndex) {
                                    case 0:
                                        return this.remainingHours - (+tooltipItems.yLabel) + ' hr';
                                    case 1:
                                        return this.averageBurnValue + ' hr / day';
                                    default:
                                        return this.expectedBurnValue + ' hr / day';
                                        break;
                                }
                            },
                            title: function (tooltipItems) {
                                switch (tooltipItems[0].datasetIndex) {
                                    case 0:
                                        return 'Actual ' + '(' + tooltipItems[0].xLabel + ')';
                                    case 1:
                                        return 'Average (Velocity)';
                                    default:
                                        return 'Expected (Velocity)';
                                        break;
                                }
                            },
                        }
                    },
                }
            });
        },
        ChartData: function () {
            return {
                labels: this.sprint.concat(['...', '...', '...']),
                datasets: [
                    {
                        type: 'bar',
                        label: 'Actual',
                        backgroundColor: "rgba(20, 162, 200, 0.2)",
                        data: this.actualData(),
                        borderColor: 'rgba(54, 162, 200, 1)',
                        borderWidth: 2
                    }, {
                        type: 'line',
                        tension: 0,
                        label: 'Average (Velocity)',
                        backgroundColor: "rgba(255,99,132, 0)",
                        data: this.averageData(),
                        borderColor: "rgba(255,99,132,1)",
                        borderWidth: 2
                    }, {
                        type: 'line',
                        tension: 0,
                        label: 'Expected (Velocity)',
                        backgroundColor: "rgba(255,99,132, 0)",
                        data: this.expectedData(),
                        borderColor: "rgba(255, 206, 86, 1)",
                    }]
            }
        },
        generageActualData: function () {
            var remaining = this.remainingHours;
            return this.actualBurnData.map(function (x) {
                return remaining - (+x);
            });
        },
        generateAverageData: function () {
            var sum = 0;
            this.actualBurnData.forEach(function (value) {
                sum += value;
            });
            var average = sum / this.actualBurnDays;
            this.averageBurnValue = average;
            this.startWork = average > 0;
            var data = [];
            var i = 0;
            while (true && this.startWork) {
                data[i] = this.remainingHours - average * (i + 1);
                if (data[i] <= 0) break;
                i++;
            }
            return data;
        },
        generateExpectedData: function () {
            var data = [];
            data[this.actualBurnDays - 1] = this.actualData[this.actualBurnDays - 1];
            var rate = (data[this.actualBurnDays - 1] - 0) / this.remainingDay;
            this.expectedBurnValue = rate;
            for (var i = this.actualBurnDays; i < this.sprintLength - 1; i++) {
                data[i] = data[i - 1] - rate;
            }
            data[this.sprintLength - 1] = 0;
            return data;
        },
        getDatas: function () {
            return $.ajax({
                url: '/burndown/get_chart/' + this.empID,
                method: 'GET',
                data: {},
                success: $.proxy(this.load_apps, this),
            });
        },
    });
    return {
        ImpGraph: ImpGraph
    };
});
