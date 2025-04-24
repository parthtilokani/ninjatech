
import { Component, onWillRender, onWillUpdateProps, useState } from "@odoo/owl";
import { DateTimePicker } from '@web/core/datetime/datetime_picker';
import { patch } from "@web/core/utils/patch";
import {
    MAX_VALID_DATE,
    MIN_VALID_DATE,
    clampDate,
    is24HourFormat,
    isInRange,
    isMeridiemFormat,
    today,
} from "@web/core/l10n/dates";


patch(DateTimePicker, {
    props: {
        ...DateTimePicker.props,
        type: { type: [{ value: "date" }, { value: "datetime" }, {value: "time"}], optional: true },
    },
});

patch(DateTimePicker.prototype, {

    validateAndSelect(value, valueIndex, unit) {

        if (!this.props.onSelect) {
            // No onSelect handler
            return false;
        }

        const result = [...this.values];
        result[valueIndex] = value;

        if (this.props.type === "datetime" || this.props.type === "time") {
            // Adjusts result according to the current time values
            const [hour, minute, second] = this.getTimeValues(valueIndex);
            result[valueIndex] = result[valueIndex].set({ hour, minute, second });
        }


        if (!isInRange(result[valueIndex], [this.minDate, this.maxDate])) {
            // Date is outside range defined by min and max dates
            return false;
        }
        this.props.onSelect(result.length === 2 ? result : result[0], unit);
        return true;
    }

});


