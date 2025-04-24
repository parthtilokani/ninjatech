import {
    deserializeDate,
    deserializeDateTime,
    parseDate,
    parseDateTime,
} from "@web/core/l10n/dates";
import PublicWidget from "@web/legacy/js/public/public_widget";
import { parseTime, formatTime } from "../l10/date";

export const DateTimeRangePickerWidget = PublicWidget.Widget.extend({
    selector: "[data-widget='datetime-range-picker']",
    disabledInEditableMode: true,

    /**
     * @override
     */
    start() {
        this._super(...arguments);
        const { widgetType, minDate, maxDate, value: initValue } = this.el.dataset;
        const type = widgetType || "time";
        const [parse, deserialize] = [parseTime, formatTime];

        // Determine the initial value for range mode.
        // Try to parse initValue as JSON. If not valid, use the same value for both start and end.
        let parsedValue;
        try {

                const jsonValue = JSON.parse(initValue);
                if (Array.isArray(jsonValue) && jsonValue.length === 2) {
                    parsedValue = jsonValue.map(v => parse(v));
                } else {
                    parsedValue = [parse(initValue), parse(initValue)];
                }


        } catch (err) {
            parsedValue = [parse(initValue), parse(initValue)];
        }

        // Define a getInputs function that returns the two input elements.
        const getInputs = () => {
            // We expect both date inputs to have the class "o_datepicker_input"
            return Array.from(this.el.querySelectorAll("input.o_datepicker_input")).slice(0, 2);
        };
        if (getInputs()){
            this.disableDateTimePicker = this.call("datetime_picker", "create", {
                target: this.el,
                pickerProps: {
                    type: type,
                    value: parsedValue, // an array of two date values
                    range: true,
                },
            }, getInputs).enable();
        } else {
            this.disableDateTimePicker = this.call("datetime_picker", "create", {
                target: this.el,
                pickerProps: {
                    type: type,
                    value: parsedValue, // an array of two date values
                    range: true,
                },
            }).enable();
        }


        // Get user timezone
        const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

        // Create or update a hidden input field for the timezone
        let timezoneInput = this.el.querySelector("input[name='user_timezone']");
        if (!timezoneInput) {
            timezoneInput = document.createElement("input");
            timezoneInput.type = "hidden";
            timezoneInput.name = "user_timezone";
            this.el.appendChild(timezoneInput);
        }
        if (!timezoneInput.value){
            timezoneInput.value = userTimeZone;
        }


    },

    /**
     * @override
     */
    destroy() {
        this.disableDateTimePicker();
        return this._super(...arguments);
    },
});


PublicWidget.registry.DateTimeRangePickerWidget = DateTimeRangePickerWidget;
