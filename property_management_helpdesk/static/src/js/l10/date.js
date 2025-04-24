const { DateTime, Settings } = luxon;
import { localization } from "@web/core/l10n/localization";

export function parseTime(value, options = {}) {

    if (!value) {
        return false;
    }

    const fmt = options.format || localization.timeFormat; // Default format for parsing
    const parseOpts = {
        setZone: true,
        zone: options.tz || "default",
    };
    const switchToLatin = Settings.defaultNumberingSystem !== "latn" && /[0-9]/.test(value);

    // Force numbering system to latin if actual numbers are found in the value
    if (switchToLatin) {
        parseOpts.numberingSystem = "latn";
    }

    // Base case: try parsing with the given format and options
    let result = DateTime.fromFormat(value, fmt, parseOpts);

    if (!result.isValid) {
        throw new Error(`'${value}' is not a valid time format`);
    }

    return result.setZone(options.tz || "default");




}

export function formatTime(value, options = {}) {

    if (!value) {
        return "";
    }

    let format = options.format;
    if (!format) {
        format = `${localization.timeFormat}`;
    }

    if (options.condensed) {
        format = getCondensedFormat(format);
    }
    return value.setZone(options.tz || "default").toFormat(format);
}
