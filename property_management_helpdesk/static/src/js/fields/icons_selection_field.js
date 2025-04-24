/** @odoo-module **/

import { Component, useRef, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import  { SelectionField, selectionField } from "@web/views/fields/selection/selection_field"


export class IconSelectionField extends SelectionField {

    static props = {
        ...SelectionField.props,
        colors: { type: Object },
        icon: { type: String },
    }


    setup(){
        super.setup();
        const readonlyRef = useRef("readonlyRef");
        const selectRef = useRef("selectRef");

        onMounted(() => {
            const colors = this.props.colors;
            const defaultIcon = this.props.icon;

            if (selectRef.el){
                new TomSelect(selectRef.el, {
                    controlInput: null,
                    render: {
                      option: function(data, escape) {
                        const colorClass = colors[JSON.parse(data.value)];
                        const icon = JSON.parse(data.value) ? defaultIcon : '';
                        return `<div><i class="fa ${icon} me-1 ${colorClass}"></i>${escape(data.text)}</div>`;
                      },
                      item: function(data, escape) {
                        const colorClass = colors[data.value] || 'text-muted';
                        const icon = JSON.parse(data.value) ? defaultIcon : '';
                        return `<div><i class="fa ${icon} me-1 ${colorClass}"></i>${escape(data.text)}</div>`;
                      }
                    }
                });
            }
            else if (readonlyRef.el){
                const colorClass = colors[this.value];
                const icon = this.value ? defaultIcon : '';
                const iconElement = document.createElement('i');
                iconElement.className = `fa ${icon} ${colorClass} me-1`;
                readonlyRef.el.prepend(iconElement);
            }

        });
    }
    _getLabelFromValue(val) {
        const selection = this.field.selection;
        const match = selection.find(([k, v]) => k === val);
        return match ? match[1] : val;
    }



}

export const iconSelectionField = {
    component: IconSelectionField,
    displayName: _t("IconSelection"),
    supportedTypes: ["selection"],
    extractProps: (fieldInfo, dynamicInfo) => ({
        ...selectionField.extractProps(fieldInfo, dynamicInfo),
        colors : fieldInfo.options.colors,
        icon : fieldInfo.options.icon,
    }),
}

registry.category("fields").add("icon_selection", iconSelectionField);