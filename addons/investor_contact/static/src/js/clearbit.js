odoo.define('investor_contact.clearbit', function (require) {
	'use strict';

	var FieldClearbit = require('web_clearbit.field'),
		concurrency = require('web.concurrency');

	FieldClearbit.include({
		init: function () {
			var self = this;
			
        	self._super.apply(self, arguments);
	        if (-1 === ['res.partner','crm.lead'].indexOf(self.model)) {
	            return;
	        }
	        if (self.mode === 'edit') {
	            self.tagName = 'div';
	            self.className += ' dropdown open';
	        }
	        if (self.debounceSuggestions > 0) {
	            self._suggestCompanies = _.debounce(self._suggestCompanies.bind(self), self.debounceSuggestions);
	        }
	        self._clearbitDropPrevious = new concurrency.DropPrevious();
	    },
	});

});