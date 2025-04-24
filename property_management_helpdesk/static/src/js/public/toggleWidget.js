import PublicWidget from "@web/legacy/js/public/public_widget";


export const  ToggleWidget = PublicWidget.Widget.extend({
        // Bind this widget to each checkbox with class toggle-checkbox
        selector: '.toggle-checkbox',
        disabledInEditableMode: false,

        /**
         * @override
         */
        start: function () {
            console.log('here??????????????? start???');
            this._super.apply(this, arguments);
            // Read the data-target attribute to know which element to toggle.
            // For example, data-target="#myContent" or ".toggle-content"
            var targetSelector = this.$el.data('target');
            if (!targetSelector) {
                console.warn("No data-target specified for toggle-checkbox", this.$el);
                return Promise.resolve();
            }
            // Find the target element in the document
            this.$target = $(targetSelector);
            if (!this.$target.length) {
                console.warn("Target element not found for selector:", targetSelector);
                return Promise.resolve();
            }
            const toggleRequired = (isChecked) => {
                console.log("isChecked..........", isChecked);
                this.$target.find("input").each(function () {
                    if (isChecked) {
                        $(this).addClass("s_website_form_model_required").attr("required", true);
                        $(this).removeClass("d-none");
                    } else {
                        $(this).addClass("d-none");
                        $(this).removeClass("s_website_form_model_required").removeAttr("required");
                    }
                });
            };
            // Hide the target initially if the checkbox is not checked
            console.log("initial............", this.$el.is(':checked'))
            if (!this.$el.is(':checked')) {
                console.log('here??????????????? start???');
                this.$target.show();
                toggleRequired(true);
            }
            // Bind change event to toggle target visibility
            this.$el.on('change', () => {
                if (!this.$el.is(':checked')) {
                    console.log('here???????????????');
                    this.$target.show();
                    toggleRequired(true);
                    this.$target.trigger('widget:refresh');
                } else {
                    this.$target.hide();
                    toggleRequired(false);
                    this.$target.trigger('widget:refresh');
                }
            });
            return Promise.resolve();
        },
    });

PublicWidget.registry.ToggleWidget = ToggleWidget;
return ToggleWidget;


